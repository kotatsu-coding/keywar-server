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

    colors = ['red', 'blue', 'green', 'black']

    def __init__(self):
        pass

    def to_dict(self):
        return {
            'id': self.id,
            'users': [user.to_dict() for user in self.users]
        }

    def join(self, user):
        user.color = self._pick_color()
        self.users.append(user)
        join_room(self.id)
        print(user, 'JOINED')
        self.send_message('users', {
            'users': [user.to_dict() for user in self.users]
        })

    def leave(self, user):
        self.users.remove(user)
        leave_room(self.id)
        self.send_message('users', {
            'users': [user.to_dict() for user in self.users]
        })

    def send_message(self, event, data=None, include_self=True):
        print('SEND MESSAGE', request.sid)
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

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'color': self.color,
            'is_host': self.hosting_room is not None
        }
