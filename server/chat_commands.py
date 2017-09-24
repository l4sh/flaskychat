"""
    server/chat_commands.py
    Chat command handler
"""
from datetime import datetime
from flask import session
from flask_socketio import rooms
from .senders import Sender

send = Sender()

class CommandHandler(object):
    """
    Handle chat commands execution
    """

    def run(self, command, *args):
        """
        Check if command exists and run it
        """
        command = command.lower()

        if callable(getattr(self, command, None)):
            getattr(self, command)(*args)
            return

        send.error_message("Command '{}' not found".format(command))

    def rooms(*args):
        """
        Return list of available rooms
        """
        send.system_message('\n'.join(rooms()))

    def date(*args):
        """
        Respond with current date and time
        """
        current_date = datetime.now().isoformat(' ').split('.')[0]
        send.system_message(current_date)

    def slap(slapped, *args):
        """
        Sends the classic message:
            'Alice slaps Bob around a bit with a large trout'
        """
        nick = session.get('nick', 'Flaskychat')
        message = ('{} slaps {} around a bit with a '
                   'large trout').format(nick, slapped)
        send.system_message(message, broadcast=True)

