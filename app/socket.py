from pprint import pprint

from flask import jsonify, request
from app import socketio, db
from app.models import room, User, Game, Word

#################### connection
@socketio.on('disconnect')
def disconnect():
    room.user_leave(request.sid)
    print(f'# user disconnected: {User.get_current_user()}')
    print(f'# remaining users: {room.users}')

##################### lobby
@socketio.on('user join')
def handle_user_join(data):
    print(f"# user joined: {data['username']}")
    user = room.user_join(request.sid, data['username'])
    if user is None:
        handle_error('인원초과입니다')
        return

    db.session.add(user)
    db.session.commit()
    
    current_users = room.get_users()
    send_current_users(current_users)
    #send_current_game_info()

def send_current_users(users):
    print("send current users")
    socketio.emit('current users', {
        'users': [user.to_dict() for user in users]
    })

@socketio.on('add word')
def handle_add_word(data):
    print(f"# new word added: {data['word']}")
    word = Word(data['word'])
    msg = word.write_word_to_file()
    handle_error(msg)
    # db.session.add(word)
    # db.session.commit()

####################### gameplay
@socketio.on('game start')
def handle_start(data):
    # num_users 일치 안하면 게임 시작x
    room.game = Game(data['game_time'], room.users)
    print('game start')
    send_current_game_info()
    socketio.emit('server game start')

@socketio.on('stroke key')
def handle_stroke_key(key):
    print(f'# stroke key event: {User.get_current_user()} pushed {key}')
    team = room.game.get_current_team()
    user = User.get_current_user()
    word = team.get_current_word()
    current_index = team.stroke_key(key, user.color)
    if current_index == len(word.value):
        team.show_next_word()
    send_current_game_info()

def send_current_game_info():
    pprint(room.game.to_dict())
    socketio.emit('current game info', {
        'game': room.game.to_dict()
    })

######################## error handling
def handle_error(error_msg):
    socketio.emit('error', {"msg": error_msg})
