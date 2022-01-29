from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_migrate import Migrate

migrate = Migrate()
socketio = SocketIO()
db = SQLAlchemy()

def create_app():
    app = Flask(__name__, static_folder='../build', static_url_path='/')
    app.config['SECRET_KEY'] = 'secret!'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['CORS_HEADERS'] = 'Content-Type'
    db.init_app(app)
    migrate.init_app(app, db)
    socketio.init_app(app, cors_allowed_origins='*')

    from app.socket import LobbyNamespace, RoomNamespace
    socketio.on_namespace(LobbyNamespace('/lobby'))
    socketio.on_namespace(RoomNamespace('/room'))
    return app

app = create_app()

from app import models
from app import route
from app import socket
