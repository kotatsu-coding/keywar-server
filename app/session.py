from uuid import uuid4
from werkzeug.local import LocalProxy
from flask import _request_ctx_stack, _app_ctx_stack, request
from app.models import User


def get_current_user():
    import random
    top = _request_ctx_stack.top
    if not hasattr(top, 'keywar_current_user'):
        top.keywar_current_user = random.random()
    return top.keywar_current_user

'''
def get_current_user():
    top = _app_ctx_stack.top
    if not hasattr(top, 'keywar_current_user'):
        # user = User.query.filter_by(sid=request.sid).first()
        top.keywar_current_user = uuid4()
    return top.keywar_current_user
'''

def get_current_room():
    top = _app_ctx_stack.top
    if not hasattr(top, 'keywar_current_room'):
        current_user = User.query.filter_by(sid=request.sid).first()
        room = current_user.room
        top.keywar_current_room = room 
    return top.keywar_current_room


current_user = LocalProxy(get_current_user)
current_room = LocalProxy(get_current_room)