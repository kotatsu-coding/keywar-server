from app.api import bp
from app.errors import error_response
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


@bp.route('/users/me', methods=['GET'])
def get_me():
    def get_token():
        auth = request.headers.get('Authorization')
        if auth and 'Bearer' in auth:
            token = auth.split('Bearer ')[1]
            return token
        return None

    token = get_token()

    if token is None:
        return error_response(401)

    user = User.check_token(token)
    if user is None:
        return error_response(401)

    return {
        'user': user.to_dict(include_token=True)
    }
