from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_cors import CORS
from flask_migrate import Migrate

app = Flask(__name__)
# CORS(app)
app.config['SECRET_KEY'] = 'secret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')
socketio = SocketIO(app, cors_allowed_origins="*")

from app import models
from app import route
from app import socket
