from .flask import app
from flask_socketio import SocketIO, emit

socketio = SocketIO(app)

def message(home_team, away_team, game_time, message, home_team_score=-1, away_team_score=-1):
    """
    Send a message to client via sockets
    !!Arguments may change soon!!

    Keyword arguments:
    teamA, teamB, teamAScore, teamBScore, gameTime, msg
    """
    socketio.emit("message", {'homeTeam': home_team, 'awayTeam': away_team, 'gameTime': game_time, 'message': message, 'homeTeamScore': home_team_score, 'awayTeamScore': away_team_score})

def fakemsg():
    """
    Send some fake messages via sockets to client
    """
    message("FC Barcalona", "FC Cincinnati", "0'", "Lionel Messi scored!",  0, 0)
    message("FC Barcalona", "FC Cincinnati", "1'", "Lionel Messi scored!",  1, 0)
    message("FC Barcalona", "FC Cincinnati", "3'", "Lionel Messi scored!", 2, 0)
    print("Fake messages sent to client")
