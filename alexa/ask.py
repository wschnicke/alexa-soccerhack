import logging, configparser, datetime, json
import alexa.api_requests
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
    #TODO handle games determined by penalty kicks
    team_info = get_team(team)
    team_id = team_info[0]
    side = "away"
    match_id = alexa.api_requests.get_last_match_id(str(team_id))
    #guard clause for no match found
    if(match_id == -1):
        speech_text = render_template('no_match_found_last_year', team=team_info[1])
        return statement(speech_text)

    match_details = alexa.api_requests.request_match_details(str(match_id))
    if(team_id == match_details['homeTeam']['dbid']):
        team_name = match_details['homeTeam']['name']
        opponent = match_details['awayTeam']['name']
        team_score = match_details['homeGoals']
        opp_score = match_details['awayGoals']
    else:
        team_name = match_details['awayTeam']['name']
        opponent = match_details['homeTeam']['name']
        team_score = match_details['homeGoals']
        opp_score = match_details['awayGoals']

    #determine winner
    template = 'draw'
    if side == match_details['outcome']['winner']:
        template='win'
    elif match_details['outcome']['winner'] == "draw":
        template='draw'
    else:
        template='loss'
    #check for pks
    pks = ""
    if match_details['outcome']['type'] == "penalties":
        pks = "_pks"

    speech_text = render_template('last_result_' + template + pks, team=team_name, team_score=team_score, opponent=opponent, opp_score=opp_score)
    return statement(speech_text)

@ask.intent('CurrentMatchStatusIntent')
def current_match_score(team):
    #TODO: call api to get match score data, set score
    team_score=1
    opp_score=123
    opp="bad guys"
    minute ="20"

    speech_text = render_template('current_status', team=team, team_score=team_score, opponent=opp, opp_score=opp_score, minute = minute)
    return statement(speech_text)

@ask.intent('NextMatchTimeIntent')
def match_time(team):
    team_info = get_team(team)
    team_id = team_info[0]
    match_id = alexa.api_requests.get_next_fixture_id(str(team_id))
    #guard clause for no match found
    if(match_id == -1):
        speech_text = render_template('no_match_found_next_year', team = team_info[1])
        return statement(speech_text)

    match_details = alexa.api_requests.request_match_details(str(match_id))
    timestamp = match_details['start']
    timestamp = timestamp / 1000

    start_time = datetime.datetime.fromtimestamp(timestamp)
    if(team_id == match_details['homeTeam']['dbid']):
        team_name = match_details['homeTeam']['name']
        opponent = match_details['awayTeam']['name']
    else:
        team_name = match_details['awayTeam']['name']
        opponent = match_details['homeTeam']['name']

    speech_text = render_template('next_match_time', team=team_name,
        opponent=opponent, day = start_time.day, month = start_time.month,
        year = start_time.year, hour = start_time.hour,
        minutes = start_time.minute)
    return statement(speech_text)

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
