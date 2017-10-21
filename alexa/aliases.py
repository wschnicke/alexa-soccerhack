import json, codecs

data = {}

def add_alias(alias, team, team_id):
    with codecs.open('data/aliases.json', 'r+', encoding='utf-8') as f:
        # If found, alert console that it is being replaced
        if alias in data:
            print("Replacing alias: " + alias + ": " + json.dumps(data[alias]))
        # Edit dict
        data[alias] = {'id': team_id, 'name': team} # <--- add `id` value.
        # Replace file contents
        f.seek(0)        # <--- should reset file position to the beginning.
        json.dump(data, f, indent=4)
        f.truncate()     # remove remaining part
        # Alert console
        print("Added alias: " + alias + ": " + json.dumps(data[alias]))

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
        add_alias("Cinci", "FC Cincinatti", 123) # Example alias add

except FileNotFoundError:
    print("Aliases file does not exist...creating it:")
    with open(aliases_file, 'w') as f:
        print("{}", file=f)
