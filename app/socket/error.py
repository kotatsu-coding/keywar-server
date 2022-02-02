from flask_socketio import emit


def handle_error(error_msg):
    emit('error', {"msg": error_msg})

