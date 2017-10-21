from .flask import app
from flask_socketio import SocketIO, emit

socketio = SocketIO(app)

def message(teamA, teamB, teamAScore, teamBScore, gameTime, msg):
    """
    Send a message to client via sockets
    !!Arguments may change soon!!

    Keyword arguments:
    teamA, teamB, teamAScore, teamBScore, gameTime, msg
    """
    socketio.emit("message", {'teamA': teamA, 'teamB': teamB, 'teamAScore': teamAScore, 'teamBScore': teamBScore, 'gameTime': gameTime, 'msg': msg})

def fakemsg():
    """
    Send some fake messages via sockets to client
    """
    message("FC Barcalona", "FC Cincinnati", 0, 0, "0'", "Lionel Messi scored!")
    message("FC Barcalona", "FC Cincinnati", 1, 0, "1'", "Lionel Messi scored!")
    message("FC Barcalona", "FC Cincinnati", 2, 0, "3'", "Lionel Messi scored!")
    print("fake messages sent")
