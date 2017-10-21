import logging, configparser
from flask_ask import Ask, request, session, question, statement

from web.flask import app
from .aliases import *
from flask import render_template

ask = Ask(app, "/ask")
logging.getLogger('flask_ask').setLevel(logging.DEBUG)
config = configparser.ConfigParser()
config.read('config.ini')
api_key = config['DEFAULT']['APIkey']

@ask.launch
def start_soccer_stat():
    welcome_msg = "this is a test message"
    return question(welcome_msg)

@ask.intent('MatchScoreIntent')
def match_score(team):
    #TODO: call api to get match score data, set score
    one_score="1"
    two_score="123"
    opp="bad guys"
    speech_text = render_template('score', team=team, team_score=one_score, opponent=opp, opp_score=two_score)
    return statement(speech_text)

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

@ask.intent('AliasIntent')
def alias_team(alias, team):
    """Add alias to alias database, called by Alexa

    Keyword arguments:
    alias, team
    """
    add = add_alias(alias, team)
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
