from app import socketio
from app.models import room, User
from flask import request

@socketio.on('disconnect')
def disconnect():
    room.user_leave(request.sid)
    print(f'# user disconnected: {User.get_current_user()}')
    print(f'# remaining users: {room.users}')