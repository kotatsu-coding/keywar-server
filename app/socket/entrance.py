from app import db
from app.models import User
from flask import request
from flask_socketio import Namespace, emit


class EntranceNamespace(Namespace):
    def on_connect(self):
        print('ENTRANCE CONNECTED')

    def on_disconnect(self):
        print('ENTRANCE DISCONNECTED')

    def on_set_user(self, data=None):
        user = User()
        if data is not None and 'username' in data:
            user.username = data['username']
        db.session.add(user)
        db.session.commit()

        if user.username is None:
            user.username = f'Guest_{user.id}'

        db.session.commit()

        emit('set_user', {
            'user': user.to_dict(include_token=True)
        })
        