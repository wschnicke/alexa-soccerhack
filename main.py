import logging
import os
import configparser

from flask import Flask
from flask_ask import Ask, request, session, question, statement
from web.routes import routes

app = Flask(__name__,  template_folder="web/templates", static_folder="web/static")

# Front-end web logic
app.register_blueprint(routes)

# Alexa logic
app = Flask(__name__)
ask = Ask(app, "/ask")
logging.getLogger('flask_ask').setLevel(logging.DEBUG)
config = configparser.ConfigParser()
api_key = config['DEFAULT']['APIkey']

@ask.launch
def launch():
    speech_text = 'Welcome to the Alexa Skills Kit, you can say hello'
    return question(speech_text).reprompt(speech_text).simple_card('HelloWorld', speech_text)

@ask.intent('HelloWorldIntent')
def hello_world():
    speech_text = 'Hello world'
    return statement(speech_text).simple_card('HelloWorld', speech_text)

@ask.intent('AMAZON.HelpIntent')
def help():
    speech_text = 'You can say hello to me!'
    return question(speech_text).reprompt(speech_text).simple_card('HelloWorld', speech_text)

@ask.session_ended
def session_ended():
    return "{}", 200

if __name__ == '__main__':
    if 'ASK_VERIFY_REQUESTS' in os.environ:
        verify = str(os.environ.get('ASK_VERIFY_REQUESTS', '')).lower()
        if verify == 'false':
            app.config['ASK_VERIFY_REQUESTS'] = False
    app.run(debug=True)
