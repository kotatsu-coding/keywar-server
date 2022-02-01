from app import socketio, db
from app.models import User, Room

class TestLobby:
    def test_user_not_exist(self, app):
        client = socketio.test_client(app, namespace='/lobby')
        assert client.is_connected('/lobby')
        client.emit('user', {
            'id': 1
        }, namespace='/lobby')
        received = client.get_received(namespace='/lobby')
        assert len(received) == 1
        assert received[0]['name'] == 'error'

    def test_user(self, app):
        with app.app_context():
            user = User(sid='test sid')
            db.session.add(user)
            db.session.commit()

            assert user.id == 1

        client = socketio.test_client(app, namespace='/lobby')
        assert client.is_connected('/lobby')
        client.emit('user', {
            'id': 1
        }, namespace='/lobby')
        received = client.get_received(namespace='/lobby')
        assert len(received) == 1
        assert received[0]['name'] == 'user'

    def test_get_rooms_when_no_room(self, app):
        client = socketio.test_client(app, namespace='/lobby')
        assert client.is_connected('/lobby')
        client.emit('get_rooms', namespace='/lobby')
        received = client.get_received(namespace='/lobby')
        assert len(received) == 1
        assert received[0]['name'] == 'rooms'
        assert len(received[0]['args'][0]['rooms']) == 0

    def test_get_rooms(self, app):
        with app.app_context():
            room = Room()
            db.session.add(room)
            db.session.commit()
        client = socketio.test_client(app, namespace='/lobby')
        assert client.is_connected('/lobby')
        client.emit('get_rooms', namespace='/lobby')
        received = client.get_received(namespace='/lobby')
        assert len(received) == 1
        assert received[0]['name'] == 'rooms'
        assert len(received[0]['args'][0]['rooms']) == 1

    def test_create_room(self, app):
        with app.app_context():
            user = User(sid='test sid')
            db.session.add(user)
            db.session.commit()
            assert user.id == 1

        client = socketio.test_client(app, namespace='/lobby')
        assert client.is_connected('/lobby')
        client.emit('user', {
            'id': 1
        }, namespace='/lobby')

        received = client.get_received(namespace='/lobby')
        assert len(received) == 1
        client.emit('create_room', namespace='/lobby')
        received = client.get_received(namespace='/lobby')
        assert len(received) == 2
        assert received[0]['name'] == 'room'
        assert received[1]['name'] == 'rooms'

    def test_create_room_with_no_user(self,  app):
        client = socketio.test_client(app, namespace='/lobby')
        assert client.is_connected('/lobby')
        client.emit('create_room', namespace='/lobby')
        received = client.get_received(namespace='/lobby')
        assert len(received) == 1
        assert received[0]['name'] == 'error'
