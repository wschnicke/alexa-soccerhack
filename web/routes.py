from flask import Blueprint, render_template
from .sockets import fakemsg

routes = Blueprint('index', __name__)

@routes.route('/')
def index():
    fakemsg() # Call fake messages
    return render_template('index.html')
