import requests, configparser
import json
from datetime import datetime, timedelta


#TODO: figure out where we should actually get this
# get api_key
config = configparser.ConfigParser()
config.read(os.path.abspath('config.ini'))
api_key = config['DEFAULT']['APIkey']

# this script will
base_url = 'https://api.crowdscores.com/v1/'



# returns match_id of latest match for given team
def get_last_match_id(team_id: str):
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

    for match in matches:
        if match['isResult']:
            return match['dbid']
            #TODO: lol is this redundant?
            break

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
        if not match['isResult']:
            return match['dbid']
            #TODO: lol is this redundant?
            break

def get_last_match(team1_id: str, team2_id: str):
    return '0'


#TODO: update all these to not store the response
#TODO: send api_keys with headers
def request_teams(payload: dict):
    """make request of team list, returns json object
    see https://docs.crowdscores.com/#page:teams,header:teams-team-list
    payload must contain api_key field, and any other parameters needed
    """
    text = requests.get(base_url + 'teams', params=payload).text
    return json.loads(text)

def request_team_details(team_id: str, api_key: str):
    """make request of team details, returns json object
    see https://docs.crowdscores.com/#page:teams,header:teams-team-details
    """
    text = requests.get(base_url + 'teams/' + team_id + '?api_key=' + api_key).text
    return json.loads(text)

def request_matches(payload: dict):
    """ake request of matches, returns json object
    see https://docs.crowdscores.com/#page:matches,header:matches-matches-list
    payload must contain api_key field, and any other parameters needed
    """
    text = requests.get(base_url + 'matches', params=payload).text
    return json.loads(text)

def request_match_details(match_id: str, api_key: str):
    """make request of match details, returns json object
    see https://docs.crowdscores.com/#page:matches,header:matches-matches-details
    """
    text = requests.get(base_url + 'matches/' + match_id + '?api_key=' + api_key).text
    return json.loads(text)

def request_competitions(api_key: str):
    """make request of competitions, returns json object
    see https://docs.crowdscores.com/#page:competitions,header:competitions-competitions
    honestly I'm not sure why you would be doing this within the skill,
    but I included it
    """
    text = requests.get(base_url + 'competitions?api_key=' + api_key).text
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

def request_seasons(api_key: str):
    """ make request of seasons, returns json object
    this is static, so should be cached
    see https://docs.crowdscores.com/#page:seasons
    """
    text = requests.get(base_url + 'seasons?api_key=' + api_key).text
    return json.loads(text)

def request_football_states(api_key: str):
    """make request of football states, returns json object
    this is static, so should be cached
    see https://docs.crowdscores.com/#page:football-states
    """
    text = requests.get(base_url + 'football_states?api_key=' + api_key).text
    return json.loads(text)
