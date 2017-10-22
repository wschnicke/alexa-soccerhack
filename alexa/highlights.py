import requests, copy
from .api_requests import api_key, request_matches
from .teams import tracked_teams
from datetime import datetime, timedelta

tracked_matches = [] # these are ongoing matches, ideally, remove when finished
tracked_updates = []
last_track = datetime.utcnow() - timedelta(days = 5) # last_check starts at 5 days before current day, updates every call

def update_tracked_matches():
    """populate tracked ongoing matches list (tracked_matches)

    example output: [142, 123, 5434, 121] (these are match ids)
    """
    global last_track
    fromTime = last_track
    toTime = datetime.utcnow()
    for team_id in tracked_teams:
        # load params list
        payload = {'api_key': api_key,
                   'team_id': team_id,
                   'from': fromTime,
                   'to': toTime}
        #TODO: remove when multileague is implemented
        payload['competition_id'] = 2 # EPL

        matches = request_matches(payload)
        if len(matches) == 0:
            break

        for match in matches:
            #if not match['isResult']: # later, only check for live matches
            tracked_matches.append(match['dbid'])

    #last_track = toTime # Refresh last_check, later
    print (tracked_matches)
    return tracked_matches

def get_tracked_updates():
    """get all tracked updates from tracked matches list and put into updates list to be traversed later (tracked_updates)
    """


def report_updates():
    """get latested updates in object format and refresh tracked updates list
    """
    updates_to_report = copy.deepcopy(tracked_updates) # deep copy and then empty tracked_updates
    tracked_updates = []
    update_tracked_matches() # refresh tracked matches
    return updates_to_report
