from app import db, socketio


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    color = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

class Room:
    colors = ['red', 'blue', 'yellow', 'black']

    def __init__(self, num_users):
        self.users = []
        self.num_users = num_users
        self.game = None
    
    def user_join(self, user):
        if len(self.users) < self.num_users:
            user.color = self._pick_color()
            self.users.append(user)
            return user
        else:
            return None 

    def _pick_color(self):
        return Room.colors[len(self.users)]         


class Game:
    def __init__(self, game_time):
        self.game_time = game_time
        self.timer = None

    def start(self):
        socketio.emit('start', {
            'game_time': self.game_time
        })
        self.show_next_word()

    def show_next_word(self):
        # socketio.emit('word', s
        pass

room = Room(2)
