import json

# read in list of LIST_OF_LEAGUES
with open('data/league_list.json')

def get_league(league_name: str):
"""Returns tuple of [league id (int), proper team name(str)]
or None if it does not exist
"""
    league_id = None
    if league_name != None:
        for k, v in teams.items():
            if k.lower() == league_name.lower():
                league_name = k
                league_id = v;
                break

    if league_id = None:
        league_name = None:
    return [league_id, league_name]

def get_league_id(league_name: str):
"""Returns tuple of [league id (int), proper team name(str)]
or None if it does not exist
"""
    league_id = None
    if league_name != None:
        for k, v in teams.items():
            if k.lower() == league_name.lower():
                league_id = v;
                break

    return league_id
