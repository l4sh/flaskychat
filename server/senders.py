"""
    server/senders.py
    Socket event emitters
"""
from flask import session
from flask_socketio import emit

class Sender(object):
    """
    Send messages
    """

    def message(self, text, nick=None, broadcast=True, **kwargs):
        """Send message to the user(s)"""
        data = {'text': text}

        if nick:
            data['nick'] = nick

        data.update(**kwargs)
        emit('message', data, broadcast=broadcast)


    def system_message(self, text, broadcast=False):
        """Send a system message to the user(s)"""
        self.message(text, broadcast=broadcast, system=True)


    def error_message(self, text, error, broadcast=False):
        """Send an error message to the user(s)"""
        self.message(text, broadcast=broadcast, error=error)

    def nick_status(self, status='OK'):
        """Send the nick status to the user"""
        data = {
            'nick': session.get('nick'),
            'status': status
        }
        emit('nick', data, broadcast=False)

    def status_update(self, status):
        """Send status update to client"""
        emit('status', status, broadcast=False)
