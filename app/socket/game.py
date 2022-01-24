from app import socketio
from app.models import room, Game, User
from pprint import pprint

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
