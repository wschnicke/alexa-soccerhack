import requests, time
from datetime import datetime, timedelta
from .api_requests import api_key, request_matches, request_match_details
from .teams import tracked_teams
from web.sockets import message
from utils.utilities import goooal

DATE_DEFICIT = 5 # looks at this amount of updates on fresh updates / add teams
tracked_types = ["penalty", "goal", "card"]

tracked_matches = [] # these are ongoing matches, ideally, remove when finished
tracked_updates = [] # current update list that hasn't been reported yet
finished_matches = [] # matches done adding updates for
last_tracked_matches = datetime.utcnow() - timedelta(days = DATE_DEFICIT) # last_check starts at 5 days before current day, updates every call
last_tracked_updates = int(time.time() - 5 * 86400) * 1000 # last_tracked_updates starts at the sam
# !!updates is unix epoch while matches is datetime -- this is for API!!

# TODO: Figure out how to deal with untracking teams... kinda hacky logic right now

def update_tracked_matches(new_teams = [], teams = tracked_teams, from_time = last_tracked_matches):
    """populate matches list from tracked teams from last_tracked_matches to current time
    if new_team = 1, will do the last (5) day instead of from the last update

    example output: [142, 123, 5434, 121] (these are match ids)
    """
    tracked_matches_found = []
    for team_id in teams:
        from_time_temp = from_time
        if (team_id in new_teams): # Use date deficit from current time if new team(s)
            from_time_temp = datetime.utcnow() - timedelta(days = DATE_DEFICIT)

        # load params list
        payload = {'api_key': api_key,
                   'team_id': team_id,
                   'from': from_time_temp,
                   'to': datetime.utcnow()}
        payload['competition_id'] = 2 # EPL - TODO: remove when multileague is implemented

        matches = request_matches(payload)
        if len(matches) != 0:
            for match in matches:
                if (match['dbid'] not in tracked_matches and match['dbid'] not in finished_matches):
                    tracked_matches_found.append(match['dbid'])
                    tracked_matches.append(match['dbid'])

    last_tracked_matches = datetime.utcnow() # Refresh last_check, later
    #print ("Tracked matches update: " + str(tracked_matches))
    return tracked_matches_found # return relevant matches

def get_tracked_updates(new_matches = [], matches = tracked_matches):
    """get all tracked updates from tracked matches list and put into updates list to be traversed later (tracked_updates)
    if new_team = 1, will do the last 5 days instead of from the last update
    """
    global last_tracked_updates
    for match_id in matches:
        # load params list
        json = request_match_details(str(match_id))
        if ("matchevents" in json): # loop thorugh events that are unseen
            for event in json["matchevents"]:
                if ("happenedAt" in event):
                    # if new match or haven't logged event yet, add to tracked_updates!
                    if (match_id in new_matches or event["happenedAt"] > last_tracked_updates):
                        if ("type" in event and event["type"] in tracked_types):
                            tracked_updates.append(event)
        if ("currentState" in json and json["currentState"] == 9): # remove finished game with no more updates
            if ("outcome" in json): # add a final outcome event TODO: revise to use state instead of outcome
                tracked_updates.append({
                    "type": "outcome",
                    "outcome": json["outcome"],
                    "homeGoals" : json["homeGoals"],
                    "awayGoals": json["awayGoals"],
                    "homeTeam": json["homeTeam"],
                    "awayTeam": json["awayTeam"]
                })
            tracked_matches.remove(match_id) # remove match from tracking list since it's over
            finished_matches.append(match_id)
    last_tracked_updates = int(time.time()) * 1000
    return tracked_updates

def update_highlights(new_teams = []):
    """get latested updates in object format and return the new count
    """
    new_matches = update_tracked_matches(new_teams)
    updates_to_report = get_tracked_updates(new_matches) # get updates
    return len(updates_to_report) # returns new size of updates

def report_updates():
    """obtain latest updates and return them
    """
    global tracked_updates
    update_highlights()
    updates = []
    if (len(tracked_updates) > 0):
        updates = list(tracked_updates)
        for event in updates:
            parse_event(event)
        tracked_updates = []
    return updates

def parse_event(event):
    #now = datetime.today().strftime('%H:%M:%S') #not needed right now
    if ('type' in event):
        if ('matchTimeString' in event):
            match_time = event['matchTimeString']
            home_team = event['homeTeam']['name']
            away_team = event['awayTeam']['name']
            if (event['type'] == 'goal'):
                scoring_team = home_team if (event['scoringSide'] == 'H') else away_team
                if (event['ownGoal']):
                    msg = "OWN " + goooal() + " for " + scoring_team + " by " + event['scoringPlayer']
                else:
                    msg = goooal() + " for " + scoring_team + " by " + event['scoringPlayer']['name']
                print("GOAL: " + msg)
                message(home_team, away_team, msg, event['homeGoals'], event['awayGoals'])
                return 1
            elif (event['type'] == 'penalty'):
                # TODO
            elif (event['type'] == 'card'):
                # TODO
            else:
                # TODO
        elif ('outcome' in event):
            # TODO
            print('=====OUTCOME=====')
            print(event)
            print('=================')
    return 0

# reminder: def message(teamA, teamB, gameTime, msg, teamAScore, teamBScore)
