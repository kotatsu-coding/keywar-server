from flask_socketio import Namespace

class MainNamespace(Namespace):
    def on_connect(self):
        print('MAIN CONNECTED')

    def on_disconnect(self):
        print('MAIN DISCONNECTED')
