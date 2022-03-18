from flask_socketio import Namespace
from app.models import User
from flask import session

class MainNamespace(Namespace):
    def on_connect(self, data):
        token = data['token']
        user = User.check_token(token)
        if user is None:
            raise ConnectionRefusedError('Unauthorized!')
        session['user'] = user
        print('MAIN CONNECTED')

    def on_disconnect(self):
        print('MAIN DISCONNECTED')

    def on_test(self):
        print('TEST', session.get('user'))