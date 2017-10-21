import os

from web.flask import app
from web.routes import routes
from web.sockets import socketio

from alexa.ask import ask

# Front-end web logic
app.register_blueprint(routes)

# Main
if __name__ == '__main__':
    if 'ASK_VERIFY_REQUESTS' in os.environ:
        verify = str(os.environ.get('ASK_VERIFY_REQUESTS', '')).lower()
        if verify == 'false':
            app.config['ASK_VERIFY_REQUESTS'] = False
    socketio.run(app, debug=True)
