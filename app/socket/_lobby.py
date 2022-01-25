from app import socketio, db
from app.models import room, Word
from flask import request
from app.socket.error import handle_error

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