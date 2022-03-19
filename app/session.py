from uuid import uuid4
from werkzeug.local import LocalProxy
from flask import _request_ctx_stack, session
from app.models import User


def get_current_user():
    top = _request_ctx_stack.top
    if not hasattr(top, 'keywar_current_user'):
        token = session.get('token')
        user = User.query.filter_by(token=token).first() if token else None
        top.keywar_current_user = user
    return top.keywar_current_user

current_user = LocalProxy(get_current_user)

def get_current_room():
    top = _request_ctx_stack.top
    if not hasattr(top, 'keywar_current_room'):
        room = current_user.room if current_user else None
        top.keywar_current_room = room 
    return top.keywar_current_room

current_room = LocalProxy(get_current_room)