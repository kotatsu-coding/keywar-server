from app import socketio
from app.models import User

class TestEntrance:
    def test_enter_with_username(self, app):
        client = socketio.test_client(app, namespace='/')
        client.emit('set_user', {
            'username': 'Test User'
        })
        with app.app_context():
            user = User.query.filter_by(username='Test User').first()
            assert user is not None


    def test_enter_as_a_guest(self, app):
        client = socketio.test_client(app, namespace='/')
        client.emit('set_user')
        with app.app_context():
            user = User.query.filter_by(username='Guest_3').first()
            assert user is not None

