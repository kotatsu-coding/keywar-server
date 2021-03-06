from app import db
from app.models import User, Room
from app.session import current_user
from flask import request
from flask_socketio import Namespace, emit

class LobbyNamespace(Namespace):
    def on_connect(self):
        pass

    def on_disconnect(self):
        pass

    def on_user(self, data):
        user_id = data['id']
        user = User.query.filter_by(id=user_id).first()
        user.sid = request.sid
        db.session.commit()

        emit('user', {
            'user': user.to_dict()
        })

    def on_get_rooms(self):
        rooms = Room.query.all()
        emit('rooms', {
            'rooms': [room.to_dict() for room in rooms]
        })

    def on_create_user(self):
        print('CREATE USER')
        user = User(sid=request.sid)
        db.session.add(user)
        db.session.commit()

        if user.username is None:
            user.username = f'Guest_{user.id}'

        db.session.commit()

        emit('user', {
            'user': user.to_dict()
        })
        rooms = Room.query.all()
        emit('rooms', {
            'rooms': [room.to_dict() for room in rooms]
        }, broadcast=True, namespace='/lobby')

    def on_create_room(self):
        room = Room()
        room.host = current_user
        db.session.add(room)
        db.session.commit()
        print(room.users)
        
        emit('room', {
            'room_id': room.id
        })

        rooms = Room.query.all()
        emit('rooms', {
            'rooms': [room.to_dict() for room in rooms]
        }, broadcast=True, namespace='/lobby')


