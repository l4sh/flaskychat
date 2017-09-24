"""
    server/events.py
    SocketIO event handlers
"""
import re
from flask import session, request, logging
from flask_socketio import SocketIO, join_room
from .senders import Sender
from .chat_commands import CommandHandler


socketio = SocketIO()
command = CommandHandler()
send = Sender()


@socketio.on('connect')
def handle_connect():
    message = 'You are now connected to {}'
    message = message.format(request.host)
    send.system_message(message)
    if not session.get('nick'):
        nick_message = ('You have not identified yourself. To chat with '
                        'other users you have to set a nick using the '
                        '/nick command.')
        send.system_message(nick_message)

@socketio.on('message')
def handle_message(data):
    if not session.get('nick'):
        message = (
            'You must select a valid nick by running the /nick command. '
            'If you need assistance run the /help command.')
        send.error_message(message, error='UNIDENTIFIED_USER')
        return

    text = data.get('text', '')
    if text.startswith('/'):
        command.run(*text.lstrip('/').split(' '))
        return

    nick = session.get('nick')
    send.message(text, nick)


@socketio.on('nick')
def handle_nick(data):
    """
    Handle setting user nick
    It receives a nick event, if the nick is OK to use
    it responds with a nick event and status
    """
    if (not data.get('nick') or
        not re.match(r'^[a-z0-9_]+$', data.get('nick', ''))):
        send.error_message(
            'You must enter a valid nick',
            'INVALID_NICK')
        return

    old_nick = session.get('nick')
    new_nick = data.get('nick')
    session['nick'] = new_nick
    broadcast = True
    message = '{} is now {}'.format(old_nick, new_nick)

    if not old_nick:
        broadcast = False
        message = 'You are connected as {}'.format(new_nick)

    send.nick_status(status='OK')
    send.system_message(message, broadcast=broadcast)


@socketio.on('join')
def handle_join(data):
    nick = session.get('nick')

    if not nick:
        message = (
            'You must select a valid nick by running the /nick command. '
            'If you need assistance run the /help command.')
        send.error_message(message, error='UNIDENTIFIED_USER')
        return

    room = data.get('room')
    join_room(room)
    send.system_message(
        '{} has joined the room {}'.format(nick, room), broadcast=True)
