from app import db
from app.models import Room


class TestLobby:
    def test_user_not_exist(self, lobby_client):
        lobby_client.emit('user', { 'id': 3 }, namespace='/lobby')
        received = lobby_client.get_received(namespace='/lobby')
        assert len(received) == 1
        assert received[0]['name'] == 'error'


    def test_user(self, lobby_client):
        lobby_client.emit('user', { 'id': 1 }, namespace='/lobby')
        received = lobby_client.get_received(namespace='/lobby')
        assert len(received) == 1
        assert received[0]['name'] == 'user'


    def test_get_rooms_when_no_room(self, lobby_user_client):
        lobby_user_client.emit('get_rooms', namespace='/lobby')
        received = lobby_user_client.get_received(namespace='/lobby')
        assert len(received) == 1
        assert received[0]['name'] == 'rooms'
        assert len(received[0]['args'][0]['rooms']) == 0


    def test_get_rooms(self, app, lobby_user_client):
        with app.app_context():
            room = Room()
            db.session.add(room)
            db.session.commit()
        lobby_user_client.emit('get_rooms', namespace='/lobby')
        received = lobby_user_client.get_received(namespace='/lobby')
        assert len(received) == 1
        assert received[0]['name'] == 'rooms'
        assert len(received[0]['args'][0]['rooms']) == 1


    def test_create_room(self, lobby_user_client):
        lobby_user_client.emit('create_room', { 'capacity': 2 }, namespace='/lobby')
        received = lobby_user_client.get_received(namespace='/lobby')
        assert len(received) == 2
        assert received[0]['name'] == 'room'
        assert received[1]['name'] == 'rooms'
        

    def test_create_room_with_no_user(self, lobby_client):
        lobby_client.emit('create_room', { 'capacity': 2 }, namespace='/lobby')
        received = lobby_client.get_received(namespace='/lobby')
        assert len(received) == 1
        assert received[0]['name'] == 'error'
