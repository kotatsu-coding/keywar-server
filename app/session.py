from werkzeug.local import LocalProxy
from flask import _app_ctx_stack, request
from app.models import User

def get_current_user():
    top = _app_ctx_stack.top
    if not hasattr(top, 'keywar_current_user'):
        user = User.query.filter_by(sid=request.sid).first()
        print('USER', user)
        if user is None:
            top.keywar_current_user = None
        else:
            top.keywar_current_user = user
    return top.keywar_current_user

def get_current_room():
    top = _app_ctx_stack.top
    if not hasattr(top, 'keywar_current_room'):
        current_user = User.query.filter_by(sid=request.sid).first()
        room = current_user.room
        top.keywar_current_room = room 
    return top.keywar_current_room


current_user = LocalProxy(get_current_user)
current_room = LocalProxy(get_current_room)