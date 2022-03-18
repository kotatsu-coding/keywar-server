from app.api import bp
from app.models import User
from app import db
from flask import request

@bp.route('/users', methods=['POST'])
def enter():
    data = request.get_json()
    username = data['username'] if 'username' in data else None
    user = User(username=username)
    db.session.add(user)
    db.session.commit()
    if user.username is None:
        user.username = f'Guest_{user.id}'
        db.session.commit()

    return {
        'user': user.to_dict(include_token=True)
    }
