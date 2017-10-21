import json, codecs
from .teams import get_team

aliases = {}

def add_alias(alias, team):
    """Adds an same into alias database

    3 = existed, 2 = replaced, 1 = success, 0 = fail

    Keyword arguments:
    alias, team
    """
    if type(alias) is not str or len(alias) < 2: # Invalid input
        return 0
    alias = alias.upper()
    team_result = get_team(team)
    if team_result == None:
        #print("Attempted alias (" + alias + ") for team (" + team + ") but team did not exist")
        return 0
    team_id = team_result[0]
    team_name = team_result[1]
    with codecs.open('data/aliases.json', 'r+', encoding='utf-8') as f:
        # If found, alert console that it is being replaced
        if alias in aliases:
            if (aliases[alias]["name"] != team):
                #print("Replacing alias: " + alias + ": " + json.dumps(aliases[alias]))
                return 2
            else:
                #print("Alias (" + alias + ") for (" + team + ") existed and was same")
                return 3
        # Edit dict
        aliases[alias] = {'id': team_id, 'name': team} # <--- add `id` value.
        # Replace file contents
        f.seek(0)        # <--- should reset file position to the beginning.
        json.dump(aliases, f, indent=4)
        f.truncate()     # remove remaining part
        # Alert console
        #print("Added alias: " + alias + ": " + json.dumps(aliases[alias]))
        return 1
    return 0

def remove_alias(alias):
    """Removes an alias if it exists

    Keyword arguments:
    alias
    """
    alias = alias.upper
    return aliases.pop(alias, None) # None here prevents the error if key is not found

def get_team_from_alias(alias):
    """Get a team ID and object given alias or return None

    Keyword arguments:
    alias
    """
    alias = alias.upper
    if alias in aliases:
        return aliases[alias]
    return None

# Load aliases file
print("Loading aliases...")
aliases_file = 'data/aliases.json'
try:
    with codecs.open(aliases_file, 'r+', encoding='utf-8') as f:
        aliases = json.load(f)
        print(str(len(aliases)) + " aliases loaded.")
except FileNotFoundError:
    print("Aliases file does not exist...creating it:")
    with open(aliases_file, 'w') as f:
        print("{}", file=f)
