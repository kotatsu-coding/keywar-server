from app import socketio

def handle_error(error_msg):
    socketio.emit('error', {"msg": error_msg})

