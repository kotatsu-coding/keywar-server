from app import socketio, db
from app.models import User, Room


class TestRoom:
    def test_user(self, room_client):
        room_client.emit('user', { 'id': 1 }, namespace='/room')
        received = room_client.get_received(namespace='/room')
        assert len(received) == 1
        assert received[0]['name'] == 'user'


    def test_join(self, lobby_user_client, room_user_client):
        lobby_user_client.emit('create_room', namespace='/lobby')
        received = lobby_user_client.get_received(namespace='/lobby')
        room_id = received[0]['args'][0]['room_id']
        assert room_id == 1

        room_user_client.emit('join', { 'room_id': room_id }, namespace='/room')
        received = room_user_client.get_received(namespace='/room')
        assert len(received) == 2
        assert received[0]['name'] == 'users'
        assert received[1]['name'] == 'joined'

 
    def test_join_when_no_room(self, room_user_client):
        room_user_client.emit('join', { 'room_id': 1 }, namespace='/room')
        received = room_user_client.get_received(namespace='/room')
        assert len(received) == 1
        assert received[0]['name'] == 'error'


    def test_join_without_user(self, app, room_client):
        with app.app_context():
            room = Room()
            db.session.add(room)
            db.session.commit()
            assert room.id == 1

        room_client.emit('join', { 'room_id': 1 }, namespace='/room')
        received = room_client.get_received(namespace='/room')
        assert len(received) == 1
        assert received[0]['name'] == 'error'


    def test_disconnect(self, app, lobby_user_client, lobby_client, room_user_client):
        lobby_user_client.emit('create_room', namespace='/lobby')
        with app.app_context():
            assert len(Room.query.all()) == 1
        _ = lobby_client.get_received(namespace='/lobby')

        room_user_client.emit('join', { 'room_id': 1 }, namespace='/room')
        _ = room_user_client.get_received(namespace='/room')
        room_user_client.disconnect(namespace='/room')

        with app.app_context():
            assert len(Room.query.all()) == 0

        received = lobby_client.get_received(namespace='/lobby')
        assert len(received) == 1
        assert received[0]['name'] == 'rooms'
        assert len(received[0]['args'][0]['rooms']) == 0
