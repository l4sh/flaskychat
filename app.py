from flask import Flask, render_template
from flask_socketio import SocketIO
import logging

app = Flask(
    __name__,
    static_folder='client/dist/static',
    template_folder='client/dist')

app.config['SECRET_KEY'] = 'mysecretkey'

socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('message')
def handle_message(json):
    print('received json: ' + str(json))

if __name__ == '__main__':
    socketio.run(app)
