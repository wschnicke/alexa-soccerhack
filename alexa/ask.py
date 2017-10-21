import logging, configparser
from flask import render_template
from flask_ask import Ask, request, session, question, statement

from web.flask import app
from .aliases import *
from .teams import *

ask = Ask(app, "/ask")
logging.getLogger('flask_ask').setLevel(logging.DEBUG)
config = configparser.ConfigParser()
config.read('config.ini')
api_key = config['DEFAULT']['APIkey']

@ask.launch
def start_soccer_stat_intent():
    welcome_msg = "this is a test message"
    return question(welcome_msg)

@ask.intent('MatchScoreIntent')
def match_score_intent(team):
    #TODO: call api to get match score data, set score
    one_score="1"
    two_score="123"
    opp="bad guys"
    speech_text = render_template('score', team=team, team_score=one_score, opponent=opp, opp_score=two_score)
    return statement(speech_text).simple_card("Match Score", speech_text)

@ask.intent('HelloWorldIntent')
def hello_world_intent():
    speech_text = 'Hello world'
    return statement(speech_text).simple_card('HelloWorld', speech_text)

@ask.intent('HelpIntent')
def help_intent():
    """Offer relevant help for HelpIntent
    """
    speech_text = 'You can say hello to me!'
    return question(speech_text).reprompt(speech_text).simple_card('HelloWorld', speech_text)

@ask.intent('AliasIntent')
def alias_team_intent(alias, team):
    """Add alias to alias database, called by Alexa

    Keyword arguments:
    alias, team
    """
    add = add_alias(alias, team)
    result = 'fail'
    if add == 1:
        result = 'success'
    elif add == 2:
        result = 'replace'
    elif add == 3:
        result = 'same'
    speech_text = render_template('alias_' + result, alias=alias, team=team)
    return statement(speech_text).simple_card("Alias", speech_text)

# TODO: Make these work with aliases!
@ask.intent('TrackTeamIntent')
def track_team_intent(team):
    get_team = get_team(team)
    result = 'error'
    if (track_id != None):
        team = get_team[1] # replace with proper name
        track = track_team(get_team[0]) # track with ID
        if (track != None):
            result = 'success'
    speech_text=render_template('track_error', team=team)
    return statement(speech_text).simple_card("Track Team", speech_text)

@ask.intent('UntrackTeamIntent')
def untrack_team_intent(team):
    team_id = get_team_id(team)


@ask.session_ended
def session_ended():
    return "{}", 200
