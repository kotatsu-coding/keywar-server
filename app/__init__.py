from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_migrate import Migrate
from flask_session import Session

migrate = Migrate()
socketio = SocketIO()
db = SQLAlchemy()
session = Session()

def create_app(test_config=None):
    app = Flask(__name__, static_folder='../build', static_url_path='/')
    app.config['SECRET_KEY'] = 'secret!'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

    if test_config:
        app.config.update(test_config)
    db.init_app(app)
    migrate.init_app(app, db)
    socketio.init_app(app, cors_allowed_origins='*')
    session.init_app(app)

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    from app.socket import MainNamespace, LobbyNamespace, RoomNamespace
    socketio.on_namespace(MainNamespace('/'))
    socketio.on_namespace(LobbyNamespace('/lobby'))
    socketio.on_namespace(RoomNamespace('/room'))
    return app

app = create_app()

@app.before_request
def before_request():
    from app.session import current_user
    print('BEFORE REQUEST', current_user)

from app import models
from app import route
from app import socket
