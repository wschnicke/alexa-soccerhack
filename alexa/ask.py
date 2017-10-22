import logging, configparser, datetime, json
import alexa.api_requests
import time
from flask import render_template
from flask_ask import Ask, request, session, question, statement

from web.flask import app
from .aliases import *
from .teams import *
from .highlights import report_updates

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
    team_info = get_team(team)
    #guard clause for no team found
    if(team_info == None):
        speech_text = render_template('error_finding_team')
        return statement(speech_text)

    team_id = team_info[0]
    match_id = alexa.api_requests.get_last_match_id(str(team_id))
    #guard clause for no match found
    if(match_id == -1):
        speech_text = render_template('no_match_found_last_year', team=team_info[1])
        return statement(speech_text)

    match_details = alexa.api_requests.request_match_details(str(match_id))
    side = "away"
    if(team_id == match_details['homeTeam']['dbid']):
        team_name = match_details['homeTeam']['name']
        opponent = match_details['awayTeam']['name']
        team_score = match_details['homeGoals']
        opp_score = match_details['awayGoals']
        side = "home"
    else:
        team_name = match_details['awayTeam']['name']
        opponent = match_details['homeTeam']['name']
        team_score = match_details['awayGoals']
        opp_score = match_details['homeGoals']

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

    speech_text = render_template('last_result_' + template + pks,
        team=team_name, team_score=team_score, opponent=opponent,
        opp_score=opp_score)
    return statement(speech_text)

@ask.intent('CurrentMatchStatusIntent')
def current_match_score(team):
    team_info = get_team(team)
    if(team_info == None):
        speech_text = render_template('error_finding_team')
        return statement(speech_text)
    team_id = team_info[0]
    match = alexa.api_requests.get_ongoing_matches(str(team_id))
    #guard clause for no match found
    if(len(match) == 0):
        speech_text = render_template('no_current_match', team=team_info[1])
        return statement(speech_text)
    #assuming a team can't play more than one game at once
    match_id = match[0]['dbid']
    match_details = alexa.api_requests.request_match_details(str(match_id))

    current_state = match_details['currentState']
    if(team_id == match_details['homeTeam']['dbid']):
        team_name = match_details['homeTeam']['name']
        opponent = match_details['awayTeam']['name']
        team_score = match_details['homeGoals']
        opp_score = match_details['awayGoals']
    else:
        team_name = match_details['awayTeam']['name']
        opponent = match_details['homeTeam']['name']
        team_score = match_details['awayGoals']
        opp_score = match_details['homeGoals']

    #TODO 50% chance of time zone error here but I'm to tired to figure it out.
    minute = 0
    #find current minute if necessary
    if(current_state == 1 or current_state == 3 or current_state == 5 or current_state == 7):
        state_start_time = match_details['currentStateStart']
        state_start_time = state_start_time / 1000
        current_time = time.time()
        minute = int((current_time - state_start_time) / 60)
        if(current_state == 3):
            minute = minute + 45
        elif(current_state == 5):
            minute = minute + 90
        elif(current_state == 7):
            minute = minute + 105

    template = "tied_"
    if(opp_score > team_score):
        template = "losing_"
    elif(team_score > opp_score):
        template = "winning_"
    else:
        template = "tied_"
    speech_text = render_template('current_status_' + template + str(current_state), team=team,
        team_score=team_score, opponent=opponent, opp_score=opp_score, minute = minute)
    return statement(speech_text)

@ask.intent('NextMatchTimeIntent')
def match_time(team):
    team_info = get_team(team)
    if(team_info == None):
        speech_text = render_template('error_finding_team')
        return statement(speech_text)
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
    # TODO: Add reprompt on fail
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

@ask.intent('HighlightsIntent')
def highlights_intent(): # TODO: Add highlights for specific team search
    updates = report_updates()
    speech_text = ""
    if len(updates) == 0:
        speech_text = render_template("no_highlights")
    else:
        for update in updates:
            print(update)
            speech_text += render_template(update["update"], **update)
    speech_text = "<speak>" + speech_text + "</speak>"
    return statement(speech_text).simple_card("Updates", speech_text)

@ask.intent('GetTeamLeagueDataIntent')
def get_team_league_data_intent(team):
    team_info = get_team(team)
    if(team_info == None):
        speech_text = render_template('error_finding_team')
        return statement(speech_text)

    team_id = team_info[0]
    #currently hardcoded to be the EPL
    league_table = alexa.api_requests.get_league_table('2')
    i = 0
    team_found = False
    team_place = None
    while(i < len(league_table) and team_found == False):
        if league_table[i]['dbid'] == team_id:
            team_place = i
            team_found = True
        i = i + 1
    if(team_found == False):
        speech_text = render_template('team_not_in_league')
        return statement(speech_text)
    team_data = league_table[team_place]
    points = team_data['points']
    wins = team_data['wins']
    losses = team_data['losses']
    draws = team_data['draws']

    speech_text = render_template('team_league_data', team=team,
        points=points, wins=wins, losses=losses, draws=draws, place=team_place)

@ask.session_ended
def session_ended():
    return "{}", 200
