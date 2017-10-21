import logging, configparser
from flask_ask import Ask, request, session, question, statement

from web.flask import app
from .aliases import *

ask = Ask(app, "/ask")
logging.getLogger('flask_ask').setLevel(logging.DEBUG)
config = configparser.ConfigParser()
config.read('config.ini')
api_key = config['DEFAULT']['APIkey']

@ask.launch
def launch():
    speech_text = 'Welcome to the Alexa Skills Kit, you can say hello'
    return question(speech_text).reprompt(speech_text).simple_card('HelloWorld', speech_text)

@ask.intent('HelloWorldIntent')
def hello_world():
    speech_text = 'Hello world'
    return statement(speech_text).simple_card('HelloWorld', speech_text)

@ask.intent('HelpIntent')
def help():
    """Offer relevant help for HelpIntent
    """
    speech_text = 'You can say hello to me!'
    return question(speech_text).reprompt(speech_text).simple_card('HelloWorld', speech_text)

@ask.intent('MatchScoreIntent')
def match_score(team):
    #TODO: call api to get match score data, set score
    speech_text = render_template('score', team=team, team_score=team_score, opponent=opponent, opp_score=opp_score)
    return statement(speech_text)

@ask.intent('AliasIntent')
def alias_team(alias, team):
    """Add alias to alias database, called by Alexa

    Keyword arguments:
    alias, team
    """
    add = add_alias(alias, team, 123456789) # TODO: Placeholder ID for now... Need to add ID logic later
    if add == 1:
        result = 'success'
    elif result == 2:
        result = 'replace'
    elif result == 3:
        result = 'same'
    else:
        result = 'fail'
    return render_template('alias_' + result, alias=alias, team=team)

@ask.session_ended
def session_ended():
    return "{}", 200
