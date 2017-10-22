import logging, configparser, datetime
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
    welcome_msg = "Welcome to Soccer Stats!"
    return question(welcome_msg)

@ask.intent('LastMatchResultIntent')
def last_match_result(team):
    #TODO get actual data
    #TODO handle games determined by penalty kicks
    if team_score > opp_score:
        speech_text = render_template('last_result_win', team=team, team_score=team_score, opponent=opponent, opp_score=opp_score)
    elif opp_score > team_score:
        speech_text = render_template('last_result_loss', team=team, team_score=team_score, opponent=opponent, opp_score=opp_score)
    else:
        speech_text = render_template('last_result_draw', team=team, team_score=team_score, opponent=opponent, opp_score=opp_score)
    return statement(speech_text)


@ask.intent('CurrentMatchStatusIntent')
def current_match_score(team):
    #TODO: call api to get match score data, set score
    team_score=1
    opp_score=123
    opp="bad guys"
    minute ="20"
    if (opp_score - team_score) > 4:
            speech_text = render_template('you_are_dead')
    else:
        speech_text = render_template('current_status', team=team, team_score=team_score, opponent=opp, opp_score=opp_score, minute = minute)
    return statement(speech_text)

@ask.intent('NextMatchTimeIntent')
def match_time(team):
    #TODO actually get the right data
    timestamp = 1508629166
    start_time = datetime.datetime.fromtimestamp(timestamp)
    opponent="bad guys"

    speech_text = render_template('next_match_time', team=team,
        opponent=opponent, day = start_time.day, month = start_time.month,
        year = start_time.year, hour = start_time.hour,
        minutes = start_time.minute)
    return statement(speech_text)

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

    Keyword arguments:liverpool next match
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
    get = get_team(team)
    result = 'fail'
    if (get != None):
        team = get[1] # replace with proper name
        track = track_team(get[0]) # track with ID
        if (track == 1):
            result = 'success'
            print("Now tracking: " + team)
            print(tracked_teams)
        else:
            result = 'already'
            print("Already tracking: " + team)
    if (result == 'fail'):
        print("Failed to track: " + team)
    speech_text=render_template('track_team_' + result, team=team)
    return statement(speech_text).simple_card("Track Team", speech_text)

@ask.intent('UntrackTeamIntent')
def untrack_team_intent(team):
    get = get_team(team)
    result = 'fail'
    if (get != None):
        team = get[1] # replace with proper name
        untrack = untrack_team(get[0]) # track with ID
        if (untrack == 1):
            result = 'success'
            print("Now untracked: " + team)
            print(tracked_teams)
        else:
            result = 'already'
            print("Already not tracked: " + team)
    if (result == 'fail'):
        print("Failed to untrack: " + team)
    speech_text=render_template('untrack_team_' + result, team=team)
    return statement(speech_text).simple_card("Untrack Team", speech_text)

@ask.session_ended
def session_ended():
    return "{}", 200
