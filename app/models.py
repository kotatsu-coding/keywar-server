import random
import datetime
from flask_socketio import join_room, leave_room, emit
from flask import request
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
    host_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    host = db.relationship('User', backref=db.backref('hosting_room', uselist=False), foreign_keys=[host_id])
    chats = db.relationship('Chat', backref='room')
    capacity = db.Column(db.Integer, default=4, nullable=False)

    colors = ['red', 'blue', 'green', 'black']

    def __init__(self, capacity=4):
        self.capacity = capacity

    def to_dict(self):
        return {
            'id': self.id,
            'teams': self.get_teams(),
            'capacity': self.capacity
        }

    def get_teams(self):
        team_1 = {
            'id': 1,
            'users': [user.to_dict(team_id=1) for user in self.users if user.color in ['red', 'blue']]
        }
        team_2 = {
            'id': 2,
            'users': [user.to_dict(team_id=2) for user in self.users if user.color in ['green', 'black']]
        }
        if self.capacity == 2:
            return [team_1]
        else:
            return [team_1, team_2]

    def join(self, user):
        user.color = self._pick_color()
        self.users.append(user)
        join_room(self.id)

    def leave(self, user):
        self.users.remove(user)
        leave_room(self.id)
        self.send_message('users', {
            'users': [user.to_dict() for user in self.users]
        })

    def send_message(self, event, data=None, include_self=True):
        print('SEND MESSAGE', request.sid, event)
        emit(event, data, to=self.id, include_self=include_self)

    def add_chat(self, user, body):
        chat = Chat(user, self, body)
        return chat

    def _pick_color(self):
        remaining_colors = [color for color in Room.colors]
        for user in self.users:
            remaining_colors.remove(user.color)
        return remaining_colors[0]


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sid = db.Column(db.String(100))
    username = db.Column(db.String(80))
    chats = db.relationship('Chat', backref='user')
    color = db.Column(db.String(100))

    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    room = db.relationship('Room', backref='users', foreign_keys=[room_id])

    def __init__(self, sid, username=None):
        self.sid = sid

    def to_dict(self, team_id=None):
        data = {
            'id': self.id,
            'username': self.username,
            'color': self.color,
            'is_host': self.hosting_room is not None
        }
        if team_id:
            data['team_id'] = team_id
        return data
