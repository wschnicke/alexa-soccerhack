import json, codecs

data = {}
team_list = {}

with open('data/team_list.json') as team_list:
    team_list = json.load(team_list)
    print ('Loaded teams list with ' + str(len(team_list)) + ' entries')

# 3 = existed, 2 = replaced, 1 = success, 0 = fail
def add_alias(alias, team):
    if team not in team_list:
        print("Attempted alias " + alias + " for " + team + " but did not exist")
        return 0
    team_id = team_list[team]
    with codecs.open('data/aliases.json', 'r+', encoding='utf-8') as f:
        # If found, alert console that it is being replaced
        if alias in data:
            if (data[alias].team == alias):
                print("Replacing alias: " + alias + ": " + json.dumps(data[alias]))
                return 2
            else:
                return 3
        # Edit dict
        data[alias] = {'id': team_id, 'name': team} # <--- add `id` value.
        # Replace file contents
        f.seek(0)        # <--- should reset file position to the beginning.
        json.dump(data, f, indent=4)
        f.truncate()     # remove remaining part
        # Alert console
        print("Added alias: " + alias + ": " + json.dumps(data[alias]))
        return 1
    return 0

# Delete alias if it exists, returning value or None
def remove_alias(alias):
    return data.pop(alias, None) # None here prevents the error if key is not found

# Get team ID and name in object given alias or return None
def get_team(alias):
    if alias in data:
        return data[alias]
    return None

# Load aliases file
print("Loading aliases...")
aliases_file = 'data/aliases.json'
try:
    with codecs.open(aliases_file, 'r+', encoding='utf-8') as f:
        data = json.load(f)
        print("Aliases loaded:")
        print(data)
except FileNotFoundError:
    print("Aliases file does not exist...creating it:")
    with open(aliases_file, 'w') as f:
        print("{}", file=f)
