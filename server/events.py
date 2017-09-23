"""
    server/events.py
    SocketIO event handlers
"""
from flask_socketio import SocketIO

socketio = SocketIO()

@socketio.on('message')
def handle_message(json):
    print('received json: ' + str(json))
    socketio.emit('message', json)
