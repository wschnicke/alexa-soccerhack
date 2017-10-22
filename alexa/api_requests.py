import requests, configparser, os
import json
from utils.utilities import get_config_path
from datetime import datetime, timedelta


#TODO: figure out where we should actually get this
# get api_key
#TODO: does this parse every time you enter
config = configparser.ConfigParser()
config.read('config.ini')
api_key = config['DEFAULT']['APIkey']

# this script will
base_url = 'https://api.crowdscores.com/v1/'

# returns match_id of latest match for given team
def get_last_match_id(team_id: str):
    #TODO CHECK IF THEY ARE IN ORDER
    """ Given a team_id, returns the most recent completed match id for team
    Returns -1 if no matches found in last year
    """
    toTime = datetime.utcnow()
    oneYear = timedelta(days = 365)
    fromTime = toTime - oneYear
    # load params list
    payload = {'api_key': api_key,
               'team_id': team_id,
               'from': fromTime,
               'to': toTime}
    #TODO: remove when multileague is implemented
    payload['competition_id'] = 2
    # get matches
    matches = request_matches(payload)
    if len(matches) == 0:
        return -1;

    #TODO: consider the following:
    #       it = reversed(matches)
    for match in reversed(matches):
        # check if match is finished
        if match['currentState'] == 9:
        #if match['isResult']:
            return match['dbid']
            #TODO: lol is this redundant?
            break
    # return -1 if no match found
    return -1

# returns match_id of latest match between 2 teams
#TODO: add pagination
def get_last_match_id_2(team1_id: str, team2_id: str):
    """ Given two team_ids, returns their most recent completed match id
    Returns -1 if no matches found in last year
    """
    toTime = datetime.utcnow()
    oneYear = timedelta(days = 365)
    fromTime = toTime - oneYear
    # load params list
    payload = {'api_key': api_key,
               'team_id': team1_id,
               'from': fromTime,
               'to': toTime}
    #TODO: remove when multileague is implemented
    payload['competition_id'] = 2
    # get matches involving team1
    matches = request_matches(payload)
    if len(matches) == 0:
        return -1;

    # TODO: not sure if we need this var
    t2_id = int(team2_id)
    # get only matches where teams are matched up
    matchups = list(filter(
        lambda x: x['awayTeam']['dbid'] == t2_id or
                  x['homeTeam']['dbid'] == t2_id,
                  matches))
    if(len(matchups) == 0):
        return -1

    #return matchups
    #TODO: consider it.reversed(matchups)

    #for i in xrange(len(matchups), 0, -1):
    for match in reversed(matchups):
        # check for finished matches
        if match['currentState'] == 9:
            return match['dbid']
            #TODO: lol is this redundant?
            break
    #return -1 if no match found
    return -1

# returns match_id of next fixture for given team
def get_next_fixture_id(team_id: str):
    """ Given a team_id, returns the next upcoming match id for team
    Returns -1 if no matches found in next year
    """
    fromTime = datetime.utcnow()
    oneYear = timedelta(days = 365)
    toTime = fromTime + oneYear
    # load params list
    payload = {'api_key': api_key,
               'team_id': team_id,
               'from': fromTime,
               'to': toTime}
    #TODO: remove when multileague is implemented
    payload['competition_id'] = 2
    # get matches
    matches = request_matches(payload)
    if len(matches) == 0:
        return -1;

    for match in matches:
        # check if match is fixture
        if match['currentState'] == 0:
            return match['dbid']
            #TODO: lol is this redundant?
            break

    #return -1 if no match found
    return -1

def get_next_fixture_id_2(team1_id: str, team2_id: str):
    """ Given two team_ids, returns their most recent completed match id
    Returns -1 if no matches found in last year
    """
    fromTime = datetime.utcnow()
    oneYear = timedelta(days = 365)
    toTime = fromTime + oneYear
    # load params list
    payload = {'api_key': api_key,
               'team_id': team1_id,
               'from': fromTime,
               'to': toTime}
    #TODO: remove when multileague is implemented
    payload['competition_id'] = 2
    # get matches involving team1
    matches = request_matches(payload)
    if len(matches) == 0:
        return -1;

    # TODO: not sure if we need this var
    t2_id = int(team2_id)
    # get only matches where teams are matched up
    matchups = list(filter(
        lambda x: x['awayTeam']['dbid'] == t2_id or
                  x['homeTeam']['dbid'] == t2_id,
                  matches))
    if(len(matchups) == 0):
        return -1

    #return matchups
    #TODO: consider it.reversed(matchups)

    #for i in xrange(len(matchups), 0, -1):
    for match in matches:
        # check if match is fiture
        if match['currentState'] == 0:
            return match['dbid']
            #TODO: lol is this redundant?
            break

    #return -1 if no match found
    return -1

#TODO: test once match is live
def get_ongoing_matches(team_id = None, competition_id = None):
    """ Return all ongoing matches; returns empty list if no ongoing matches
    Optional parameters team_id and competition_id let you specify a specific
    team or league
    """
    # get matches starting in last 6 hours
    toTime = datetime.utcnow()
    fromTime = toTime - timedelta(hours = 6)
    payload = {'api_key': api_key,
               'from': fromTime,
               'to': toTime}
    if team_id is not None:
        payload['team_id'] = team_id
    if competition_id is not None:
        payload['competition_id'] = competition_id

    matches = request_matches(payload)
    # return subset of matches that have not ended
    #TODO: make list comprehension?
    return list(filter(lambda x: 0 < x['currentState'] < 9, matches))
    #return [i for i in list if i['isResult']]

def get_league_table(competition_id: str, team_id = None):
    """ Return list of league table entries for given competition_id
    If Optional param team_id is specified, it will return just the table for
    that/those teams
    This return is the leagueTable list entity in the api
    """
    payload = {'api_key': api_key,
               'competition_id': '2'}
    if team_id is not None:
        payload['team_id'] = team_id

    tables = request_league_tables(payload)
    # ¯\_(ツ)_/¯
    return tables[0]['leagueTable']

def get_team_ids_relegation(competition_id: str):
    """ Returns list of team_ids of teams in relegation zone
    """
    table = get_league_table(competition_id)
    rel = list(filter( lambda x: x['leagueTableClass'] == 'bottom1', table))
    #TODO: improve; maybe lambda or comprehension
    result = []
    for t in rel:
        result.append(t['dbid'])
    return result

#TODO: update all these to not store the response
#TODO: send api_keys with headers
def request_teams(payload: dict):
    """make request of team list, returns json object
    see https://docs.crowdscores.com/#page:teams,header:teams-team-list
    payload must contain api_key field, and any other parameters needed
    """
    text = requests.get(base_url + 'teams', params=payload).text
    return json.loads(text)

def request_team_details(team_id: str, key=None):
    """make request of team details, returns json object
    see https://docs.crowdscores.com/#page:teams,header:teams-team-details
    """
    if key is None:
        key = api_key
    text = requests.get(base_url + 'teams/' + team_id + '?api_key=' + key).text
    return json.loads(text)

def request_matches(payload: dict):
    """ake request of matches, returns json object
    see https://docs.crowdscores.com/#page:matches,header:matches-matches-list
    payload must contain api_key field, and any other parameters needed
    """
    text = requests.get(base_url + 'matches', params=payload).text
    return json.loads(text)

def request_match_details(match_id: str, key = None):
    """make request of match details, returns json object
    see https://docs.crowdscores.com/#page:matches,header:matches-matches-details
    """
    if key is None:
        key = api_key
    text = requests.get(base_url + 'matches/' + match_id + '?api_key=' + key).text
    return json.loads(text)

def request_rounds(payload: dict):
    """make request of rounds, returns json object
    you should really only do this for a given comp
    see https://docs.crowdscores.com/#page:rounds,header:rounds-rounds
    payload must contain api_key field, and any other parameters needed
    """
    text = requests.get(base_url + 'rounds', params=payload).text
    return json.loads(text)

def request_league_tables(payload: dict):
    """make request of league tables, returns json object
    you should really only do this for a given comp
    see https://docs.crowdscores.com/#page:rounds,header:rounds-rounds
    payload must contain api_key field, and any other parameters needed
    """
    text = requests.get(base_url +'league-tables', params=payload).text
    return json.loads(text)

# After here, these requests give static information,
# which should be cached rather than called regularly

def request_competitions(key = None):
    """make request of competitions, returns json object
    see https://docs.crowdscores.com/#page:competitions,header:competitions-competitions
    honestly I'm not sure why you would be doing this within the skill,
    but I included it
    """
    if key is None:
        key = api_key
    text = requests.get(base_url + 'competitions?api_key=' + key).text
    return json.loads(text)

def request_seasons(key = None):
    """ make request of seasons, returns json object
    this is static, so should be cached
    see https://docs.crowdscores.com/#page:seasons
    """
    if key is None:
        key = api_key
    text = requests.get(base_url + 'seasons?api_key=' + key).text
    return json.loads(text)

def request_football_states(key = None):
    """make request of football states, returns json object
    this is static, so should be cached
    see https://docs.crowdscores.com/#page:football-states
    """
    if key is None:
        key = api_key
    text = requests.get(base_url + 'football_states?api_key=' + key).text
    return json.loads(text)
