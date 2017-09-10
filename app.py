from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

socketio = SocketIO(app)

@socketio.on('message')
def handle_message(json):
    print('received json: ' + str(json))

if __name__ == '__main__':
    socketio.run(app)
