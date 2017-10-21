import requests
import json

# this script will
base_url = 'https://api.crowdscores.com/v1/'

# returns json object of latest match details for given team
def get_last_match(team_id: str):
    return '0'

def get_last_match(team1_id: str, team2_id: str):
    return '0'


#TODO: update all these to not store the response
def request_teams(payload: dict):
    """make request of team list, returns json object
    see https://docs.crowdscores.com/#page:teams,header:teams-team-list
    payload must contain api_key field, and any other parameters needed
    """
    return requests.get(base_url + 'teams', params=payload).text

def request_team_details(team_id: str, api_key: str):
    """make request of team details, returns json object
    see https://docs.crowdscores.com/#page:teams,header:teams-team-details
    """
    return requests.get(base_url + 'teams/' + team_id + '?api_key=' + api_key).text

def request_matches(payload: dict):
    """ake request of matches, returns json object
    see https://docs.crowdscores.com/#page:matches,header:matches-matches-list
    payload must contain api_key field, and any other parameters needed
    """
    return requests.get(base_url + 'matches', params=payload).text

def request_match_details(match_id: str, api_key: str):
    """make request of match details, returns json object
    see https://docs.crowdscores.com/#page:matches,header:matches-matches-details
    """
    return requests.get(base_url + 'matches/' + match_id + '?api_key=' + api_key).text

def request_competitions(api_key: str):
    """make request of competitions, returns json object
    see https://docs.crowdscores.com/#page:competitions,header:competitions-competitions
    honestly I'm not sure why you would be doing this within the skill,
    but I included it
    """
    return requests.get(base_url + 'competitions?api_key=' + api_key).text

def request_rounds(payload: dict):
    """make request of rounds, returns json object
    you should really only do this for a given comp
    see https://docs.crowdscores.com/#page:rounds,header:rounds-rounds
    payload must contain api_key field, and any other parameters needed
    """
    return requests.get(base_url + 'rounds', params=payload).text

def request_league_tables(payload: dict):
    """make request of league tables, returns json object
    you should really only do this for a given comp
    see https://docs.crowdscores.com/#page:rounds,header:rounds-rounds
    payload must contain api_key field, and any other parameters needed
    """
    return requests.get(base_url +'league-tables', params=payload).text

# After here, these requests give static information,
# which should be cached rather than called regularly

def request_seasons(api_key: str):
    """ make request of seasons, returns json object
    this is static, so should be cached
    see https://docs.crowdscores.com/#page:seasons
    """
    return requests.get(base_url + 'seasons?api_key=' + api_key).text

def request_football_states(api_key: str):
    """make request of football states, returns json object
    this is static, so should be cached
    see https://docs.crowdscores.com/#page:football-states
    """
    return requests.get(base_url + 'football_states?api_key=' + api_key).text
