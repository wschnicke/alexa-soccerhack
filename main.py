import logging
import os

from flask import Flask
from flask_ask import Ask, request, session, question, statement

from web.routes import routes
s
app = Flask(__name__,  template_folder="web")

# Front-end web logic
app.register_blueprint(routes)

# Alexa logic
ask = Ask(app, "/ask")
logging.getLogger('flask_ask').setLevel(logging.DEBUG)

@ask.launch
def launch():
    speech_text = 'Welcome to the Alexa Skills Kit, you can say hello'
    return question(speech_text).reprompt(speech_text).simple_card('HelloWorld', speech_text)

@ask.intent('MatchScoreIntent')
def match_score(team):
    #TODO: call api to get match score data, set score
    speech_text = render_template('score', team=team, team_score=team_score, opponent=opponent, opp_score=opp_score)
    return statement(speech_text)

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

# Main

if __name__ == '__main__':
    if 'ASK_VERIFY_REQUESTS' in os.environ:
        verify = str(os.environ.get('ASK_VERIFY_REQUESTS', '')).lower()
        if verify == 'false':
            app.config['ASK_VERIFY_REQUESTS'] = False
    app.run(debug=True)
