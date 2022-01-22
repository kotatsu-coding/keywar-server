from flask import jsonify
from app import socketio, db
from app.models import room, User, Game

@socketio.on('user join')
def handle_user_join(data):
    user = User()
    user.username = data['username']
    user = room.user_join(user)
    if user is None:
        handle_error('인원초과입니다')
        return

    db.session.commit()
    
    current_users = room.get_users()
    send_current_users(current_users)

@socketio.on('game start')
def handle_start(data):
    room.game = Game(data['game_time'])
    pass

def handle_type(data):
    pass

def send_current_users(users):
    socketio.emit('current users', {
        'users': [user.to_dict() for user in users]
    })

def handle_error(error_msg):
    socketio.emit('error', message=error_msg)