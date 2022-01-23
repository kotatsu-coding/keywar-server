import random
import json
from datetime import datetime

from flask import request

from app import db, socketio

# class Word(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     value = db.Column(db.String(80), unique=True, nullable=False)

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
            raw_words = f.readlines()        
        words = [Word(word.strip()) for word in raw_words]
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
        self.words[0].colorize(self.users)

    def show_next_word(self):
        self.score += 1
        self.current_word_idx += 1
        if self.current_word_idx == len(self.words):
            self.current_word_idx = 0
        word = self.words[self.current_word_idx]
        return word.colorize(self.users)

    def get_current_word(self):
        return self.words[self.current_word_idx]
    
    def to_dict(self):
        return {
            'game_time': self.game_time,
            'remaining_time': self.game_time - (datetime.now() - self.started_at).total_seconds(),
            'current_word': self.words[self.current_word_idx].to_dict(),
            'users': [user.to_dict() for user in self.users],
            'score': self.score 
        }

room = Room(2)
