from app import db
from app.models import User, Room
from flask import request
from app.session import current_user, current_room
from flask_socketio import Namespace, emit
from app.game import game_manager

class RoomNamespace(Namespace):
    def on_connect(self):
        pass

    def on_disconnect(self):
        if current_room:
            current_room.leave(current_user)
            db.session.commit()
            if len(current_room.users) == 0:
                db.session.delete(current_room)
                db.session.commit()

                rooms = Room.query.all()
                emit('rooms', {
                    'rooms': [room.to_dict() for room in rooms]
                }, broadcast=True, namespace='/lobby')

    def on_user(self, data):
        user_id = data['id']
        user = User.query.filter_by(id=user_id).first()
        user.sid = request.sid
        db.session.commit()

        emit('user', {
            'user': user.to_dict()
        })

    def on_join(self, data):
        room_id = data['room_id']
        room = Room.query.filter_by(id=room_id).first()
        if len(room.users) >= 4:
            emit('room_full')
        else:
            print('A', room.users)
            room.join(current_user)
            db.session.commit() 
            emit('joined', {
                'user': current_user.to_dict()
            })

    def on_get_chats(self):
        current_room.send_message('chats', {
            'chats': [{
                'user': chat.user.to_dict(),
                'body': chat.body
            } for chat in current_room.chats]
        })

    def on_chat(self, data):
        body = data['body']
        current_room.add_chat(current_user, body)
        db.session.commit()
        current_room.send_message('chats', {
            'chats': [{
                'user': chat.user.to_dict(),
                'body': chat.body
            } for chat in current_room.chats]
        })

    def on_game_start(self):
        game = game_manager.game_start(current_room)
        current_room.send_message('game_start')
        current_room.send_message('update_game', game.teams[0].to_dict())
        current_room.send_message('update_game', game.teams[1].to_dict())

    def on_game_finished(self):
        current_room.send_message('game_finished')
        game = game_manager.get_game(current_room)
        del game

    def on_stroke_key(self, data):
        print('STROKE KEY', request.sid)
        current_word = data['current_word']
        game = game_manager.get_game(current_room)
        team = game.get_team(current_user.id)
        team.validate_word(current_word)
        if team.current_word.current_idx == len(team.current_word.value):
            team.current_word = team.show_next_word()
            current_room.send_message('update_game', team.to_dict(), include_self=True)
        else:
            current_room.send_message('update_game', team.to_dict(), include_self=False)




