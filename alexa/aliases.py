import json, codecs

data = {}

def add_alias(alias, team, team_id):
    with codecs.open('data/aliases.json', 'r+', encoding='utf-8') as f:
        data[alias] = {'id': team_id, 'name': name} # <--- add `id` value.
        f.seek(0)        # <--- should reset file position to the beginning.
        json.dump(data, f, indent=4)
        f.truncate()     # remove remaining part

# Delete alias if it exists, returning value or None
def remove_alias(alias):
    return data.pop(alias, None) # None here prevents the error if key is not found

# Get team ID and name in object given alias or return None
def get_team(alias):
    if alias in data:
        return data[alias]
    return None

print("Loading aliases...")
with codecs.open('data/aliases.json', 'r+', encoding='utf-8') as f:
    data = json.load(f)
    print("Aliases loaded:")
    print(data)
