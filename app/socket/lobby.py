from app import db
from app.models import User, Room
from app.session import current_user
from flask import request
from flask_socketio import Namespace, emit
from app.socket.error import handle_error


class LobbyNamespace(Namespace):
    def on_connect(self):
        print('LOBBY CONNECTED')

    def on_disconnect(self):
        print('LOBBY DISCONNECTED')

    def on_user(self, data):
        user_id = data['id']
        user = User.query.filter_by(id=user_id).first()
        if user is None:
            handle_error('User does not exist')
        else:
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

    def on_create_room(self, data):
        if current_user:
            room = Room(capacity=data['capacity'])
            room.host = current_user
            db.session.add(room)
            db.session.commit()
            
            emit('room', {
                'room_id': room.id
            })

            rooms = Room.query.all()
            emit('rooms', {
                'rooms': [room.to_dict() for room in rooms]
            }, broadcast=True, namespace='/lobby')
        else:
            handle_error('No user is set')
