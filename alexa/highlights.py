import requests, time
from .api_requests import api_key, request_matches, request_match_details
from .teams import tracked_teams
from datetime import datetime, timedelta

DATE_DEFICIT = 5 # looks at this amount of updates on fresh updates / add teams
TRACKED_TYPES = ["penalty", "goal", "card"]

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
                        if ("type" in event and event["type"] in TRACKED_TYPES):
                            tracked_updates.append(event)
        if ("state" in json and json["state"] == 9): # remove finished game with no more updates
            if ("outcome" in json): # add a final outcome event
                tracked_updates.append({"outcome": json["outcome"]})
            tracked_updates.remove(event) # remove match from tracking list since it's over
            finished_matches.append(match_id)
    last_tracked_updates = int(time.time()) * 1000
    return tracked_updates

def update_highlights(new_teams = []):
    """get latested updates in object format and refresh tracked updates list
    """
    new_matches = update_tracked_matches(new_teams)
    updates_to_report = get_tracked_updates(new_matches) # get updates
    return len(updates_to_report) # returns new size of updates

def report_updates():
    global tracked_updates
    update_highlights()
    updates = []
    if (len(tracked_updates) > 0):
        updates = list(tracked_updates)
        tracked_updates = []
    return updates
