import json

teams = {}

def get_team_id(team_name: str):
    """Returns teamid of given team name or None if not found
    """
    team_id = None
    for k, v in teams.items():
        if k.lower() == team_name.lower():
            team_id = v
            break
    return team_id

def get_team_name(team_id: int):
    """Given team id, return its proper name (str) or None if not found
    """
    for k, v in teams.items():
        if v == team_id:
            return k
    return None

def get_team(team_name: str):
    """Returns tuple of [team id (int), proper team name (str)] or None if it does not exist
    """
    team_id = None
    for k, v in teams.items():
        if k.lower() == team_name.lower():
            team_id = v
            team_name = k
            break
    if (team_id == None):
        return None
    return [team_id, team_name]

with open('data/team_list.json') as teams:
    teams = json.load(teams)
    print ('Loaded teams list with ' + str(len(teams)) + ' entries')
