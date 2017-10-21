from flask import Blueprint, render_template
from flask_socketio import SocketIO, emit

routes = Blueprint('index', __name__)

@routes.route('/')
def index():
    return render_template('index.html')
