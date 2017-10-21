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

@ask.session_ended
def session_ended():
    return "{}", 200
