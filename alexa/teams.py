import json

teams = {}
tracked_teams = []

def track_team(team_id: int):
    """Add team to tracking list given id
    """
    # TODO: Add highlights re-check here... or maybe in ask.pyss
    if (team_id not in tracked_teams):
        from .highlights import update_highlights # deferred import to avoid circular dependencies
        tracked_teams.append(team_id)
        update_highlights([team_id])
        return 1
    return 0

def untrack_team(team_id: int):
    """ Remove team from tracking list given id
    """
    if (team_id in tracked_teams):
        tracked_teams.remove(team_id)
        return 1
    return 0

def team_tracked(team_id: int):
    """ returns whether or not team is already tracked_teams
    """
    return team_id in tracked_teams

def get_team_name(team_id: int):
    """Given team id, return its proper name (str) or None if not found
    """
    for k, v in teams.items():
        if v == team_id:
            return k
    return None

def get_team_id(team_name: str):
    """Returns teamid of given team name or None if not found
    """
    from .aliases import get_team_from_alias # deferred import to avoid circular dependencies
    team_id = None
    found = 0
    for k, v in teams.items():
        if k.lower() == team_name.lower():
            team_id = v
            found = 1
            break
    if (not found): # If not found, try aliases list
        attempt_alias = get_team_from_alias(team_name)
        if (attempt_alias):
            team_id = attempt_alias["id"]
    return team_id

def get_team(team_name: str): # Combination of get_team_name and get_team_id
    """Returns tuple of [team id (int), proper team name (str)] or None if it does not exist
    """
    from .aliases import get_team_from_alias # deferred import to avoid circular dependencies
    team_id = None
    found = 0
    for k, v in teams.items():
        if k.lower() == team_name.lower():
            team_id = v
            team_name = k
            found = 1
            break
    if (not found): # If not found, try aliases list
        attempt_alias = get_team_from_alias(team_name)
        if (attempt_alias):
            team_id = attempt_alias[0]
            team_name = attempt_alias[1]
    if (team_id == None): # Still not found?
        return None
    return [team_id, team_name]

with open('data/team_list.json') as teams:
    teams = json.load(teams)
    print ('Loaded teams list with ' + str(len(teams)) + ' entries')
