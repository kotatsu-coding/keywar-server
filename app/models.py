import random
from datetime import datetime
from flask import request
from app import db 


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

class User(db.Model):
    id = db.Column(db.String(100), primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    color = db.Column(db.String(120), nullable=False)

    def __init__(self, id, username, color):
        self.id = id
        self.username = username
        self.color = color

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'color': self.color        
        }

    @staticmethod
    def get_current_user():
        sid = request.sid
        user = User.query.filter_by(id=sid).first()
        return user

    def __repr__(self):
        return self.username

class Room:
    colors = ['red', 'blue', 'yellow', 'black']

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


class Game:
    @staticmethod
    def generate_words():
        with open('words.txt') as f:
            words = f.read().splitlines()    
        random.shuffle(words)
        print(f'# the words are {words[:10]}')
        return words

    def __init__(self, game_time, users):
        self.game_time = game_time
        self.started_at = datetime.now()
        self.words = Game.generate_words()
        self.current_word_idx = 0
        self.users = users
        self.score = 0
        self.current_word = Word(self.words[self.current_word_idx]).colorize(self.users)
        self.sequence = []

    def stroke_key(self, key, color):
        if key == self.value[self.current_idx] \
            and self.colors[self.current_idx] == color:
            self.current_idx += 1
            self.sequence.append(color)
        else:
            self.current_idx = 0
        return self.current_idx

    def show_next_word(self):
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
            'game_time': self.game_time,
            'remaining_time': self.game_time - (datetime.now() - self.started_at).total_seconds(),
            'current_word': self.current_word.to_dict(),
            'users': [user.to_dict() for user in self.users],
            'score': self.score,
            'sequence': self.sequence
        }

room = Room(2)
