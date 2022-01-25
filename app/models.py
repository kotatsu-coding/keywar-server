import random
import datetime
from flask_socketio import join_room, leave_room, emit
from app import db 

class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    body = db.Column(db.String(300))

    def __init__(self, user, room, body):
        self.user = user
        self.room = room
        self.body = body


class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    users = db.relationship('User', backref='room')
    chats = db.relationship('Chat', backref='room')

    def __init__(self):
        pass

    def to_dict(self):
        return {
            'id': self.id,
            'users': [user.to_dict() for user in self.users]
        }

    def join(self, user):
        self.users.append(user)
        user.room = self
        join_room(self.id)
        print(user, 'JOINED')
        self.send_message('users', {
            'users': [user.to_dict() for user in self.users]
        })

    def leave(self, user):
        print(self.users)
        self.users.remove(user)
        leave_room(self.id)
        self.send_message('users', {
            'users': [user.to_dict() for user in self.users]
        })

    def send_message(self, event, data):
        print(event, data)
        emit(event, data, to=self.id)

    def add_chat(self, user, body):
        chat = Chat(user, self, body)


    def handle_message(self, data):
        pass


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sid = db.Column(db.String(100))
    username = db.Column(db.String(80))
    chats = db.relationship('Chat', backref='user')

    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))

    def __init__(self, sid, username=None):
        self.sid = sid

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username
        }


class Word:
    def __init__(self, value):
        self.value = value
        self.colors = None
        self.current_idx = 0
    
    def colorize(self, users):
        self.current_idx = 0
        source_colors = [user.color for user in users]
        self.colors = [random.choice(source_colors) for _ in range(len(self.value))]
        return self

    def stroke_key(self, key, color):
        if key == self.value[self.current_idx] \
            and self.colors[self.current_idx] == color:
            self.current_idx += 1
        else:
            self.current_idx = 0
        return self.current_idx

    def write_word_to_file(self):
        with open('words.txt') as f:
            existing_words = f.read().splitlines()
            if self.value not in existing_words:
                f.write(f'\n{self.value}')
                return f'# {self.value} added to word list'
            else:
                return f'# {self.value} is already in list'
            
    
    def to_dict(self):
        return {
            'value': self.value,
            'colors': self.colors,
            'current_idx': self.current_idx
        }

    def __repr__(self):
        return self.value



'''
class Room:
    colors = ['red', 'blue', 'purple', 'black']

    def __init__(self, num_users):
        self.users = []
        self.num_users = num_users
        self.game = None
    
    def user_join(self, sid, username):
        if len(self.users) < self.num_users:
            user = User(sid, username, self._pick_color())
            self.users.append(user)
            return user
        else:
            return None 

    def user_leave(self, sid):
        for user in self.users:
            if user.id == sid:
                self.users.remove(user)
    
    def get_users(self):
        return self.users

    def _pick_color(self):
        remaining_colors = [color for color in Room.colors]
        for user in self.users:
            remaining_colors.remove(user.color)
        return remaining_colors[0]


class Team:
    def __init__(self, words, users):
        self.current_word_idx = 0
        self.users = users
        self.score = 0
        self.words = words
        self.current_word = Word(self.words[self.current_word_idx]).colorize(self.users)
        self.sequence = []

        for user in users:
            user.team = self

    def stroke_key(self, key, color):
        self.sequence.append((color, key))
        if key == self.current_word.value[self.current_word.current_idx] \
            and self.current_word.colors[self.current_word.current_idx] == color:
            self.current_word.current_idx += 1
        else:
            self.current_word.current_idx = 0
        return self.current_word.current_idx

    def show_next_word(self):
        self.sequence = []
        self.score += 1
        self.current_word_idx += 1
        if self.current_word_idx == len(self.words):
            self.current_word_idx = 0
        self.current_word = Word(self.words[self.current_word_idx]).colorize(self.users)
        return self.current_word

    def get_current_word(self):
        return self.current_word
    
    def to_dict(self):
        return {
            'current_word': self.current_word.to_dict(),
            'users': [user.to_dict() for user in self.users],
            'score': self.score,
            'sequence': self.sequence
        }


class Game:
    @staticmethod
    def generate_words():
        with open('words.txt') as f:
            words = f.read().splitlines()    
        random.shuffle(words)
        print(f'# the words are {words[:10]}')
        return words

    @staticmethod
    def create_teams(words, users):
        teams = []
        teams.append(Team(words, users[:2]))
        teams.append(Team(words, users[2:]))
        return teams

    def __init__(self, game_time, users):
        self.game_time = game_time
        self.started_at = datetime.now()
        self.words = Game.generate_words()
        self.current_word_idx = 0
        self.teams = Game.create_teams(self.words, users)

    def get_current_team(self):
        user = User.get_current_user()
        for team in self.teams:
            for _user in team.users:
                if _user.username == user.username:
                    return team

    def to_dict(self):
        return {
            'game_time': self.game_time,
            'remaining_time': self.game_time - (datetime.now() - self.started_at).total_seconds(),
            'teams': [team.to_dict() for team in self.teams]
        }

room = Room(4)

'''