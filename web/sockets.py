from .flask import app
from flask_socketio import SocketIO, emit

socketio = SocketIO(app)

def message(teamA, teamB, teamAScore, teamBScore, gameTime, msg):
    socketio.emit("message", {'teamA': teamA, 'teamB': teamB, 'teamAScore': teamAScore, 'teamBScore': teamBScore, 'gameTime': gameTime, 'msg': msg})

def fakemsg():
    message("FC Barcalona", "FC Cincinnati", 0, 0, "0:22", "Lionel Messi scored!")
    message("FC Barcalona", "FC Cincinnati", 1, 0, "1:30", "Lionel Messi scored!")
    message("FC Barcalona", "FC Cincinnati", 2, 0, "2:30", "Lionel Messi scored!")
    print("fake messages sent")
