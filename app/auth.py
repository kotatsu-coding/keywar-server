from flask_httpauth import HTTPTokenAuth
from app.errors import error_response
from app.models import User

auth = HTTPTokenAuth()

@auth.verify_token
def verify_token(token):
    return User.check_token(token) if token else None

@auth.error_handler
def token_auth_error(status):
    return error_response(status)
