import os
import pytest
import tempfile
from app import create_app, db, socketio
from app.models import User


@pytest.fixture
def app():
    db_fp, db_path = tempfile.mkstemp()
    app = create_app(test_config={
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': f'sqlite:///{db_path}'
    })

    with app.app_context():
        db.create_all()
        user = User(sid='test sid 1')
        user.username = 'Fixture User 1'
        db.session.add(user)
        user = User(sid='test sid 2')
        user.username = 'Fixture User 2'
        db.session.add(user)
        db.session.commit()

    yield app

    os.close(db_fp)
    os.unlink(db_path)


@pytest.fixture
def lobby_client(app):
    client = socketio.test_client(app, namespace='/lobby')
    assert client.is_connected('/lobby')
    return client


@pytest.fixture
def lobby_user_client(app):
    client = socketio.test_client(app, namespace='/lobby')
    assert client.is_connected('/lobby')
    client.emit('user', { 'id': 1 }, namespace='/lobby')
    received = client.get_received(namespace='/lobby')
    assert len(received) == 1
    assert received[0]['name'] == 'user'
    return client


@pytest.fixture
def room_user_client(app):
    room_client = socketio.test_client(app, namespace='/room')
    assert room_client.is_connected('/room')
    room_client.emit('user', { 'id': 2 }, namespace='/room')
    _ = room_client.get_received(namespace='/room')
    return room_client


@pytest.fixture
def room_client(app):
    room_client = socketio.test_client(app, namespace='/room')
    assert room_client.is_connected('/room')
    return room_client
