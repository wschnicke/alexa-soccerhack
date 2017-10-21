import json

team_list = {
    'Burnley': 480,
    'Leicester City': 481,
    'Brighton and Hove Albion': 482,
    'Watford': 483,
    'Liverpool': 1,
    'Southampton': 69,
    'Chelsea': 7,
    'Stoke City': 8,
    'West Ham United': 202,
    'Manchester United': 2,
    'Everton': 12,
    'Huddersfield Town': 557,
    'Bournemouth': 558,
    'Swansea City': 15,
    'Crystal Palace': 337,
    'Arsenal': 18,
    'Newcastle United': 19,
    'Manchester City': 20,
    'West Bromwich Albion': 14,
    'Tottenham Hotspur': 13
}

file = open("team_list.json", "w")
file.write(json.dumps(team_list))
