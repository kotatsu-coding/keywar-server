from app import db
from app.models import User, Room
from flask import request
from app.game import current_user, current_room
from flask_socketio import Namespace, emit

class RoomNamespace(Namespace):
    def on_connect(self):
        pass

    def on_disconnect(self):
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
        room.join(current_user)
        db.session.commit() 
        emit('joined')

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



