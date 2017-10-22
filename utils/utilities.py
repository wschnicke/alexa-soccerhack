import os

#TODO: crazy hacky, very slow, fix later
topLevelDir = 'alexa-soccerhack'
def get_config_path():
    path = os.getcwd()
    if topLevelDir not in path:
        raise FileNotFoundError('Not in master directory, see utilites.get_config_path')

    while os.path.basename(path) != topLevelDir:
        path = os.path.dirname(path)

    return os.path.join(path, 'config.ini')
