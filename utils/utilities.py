import os
from random import randint
import jinja2

def goooal(o=0):
    """returns string of GOAL with a random number of Os unless specified number > 0
    """
    if (not o):
        o = randint(7, 25)
    return "G" + "O" * o + "AL"

#TODO: crazy hacky, very slow, fix later
topLevelDir = 'alexa-soccerhack'
def get_config_path():
    path = os.getcwd()
    if topLevelDir not in path:
        raise FileNotFoundError('Not in master directory, see utilites.get_config_path')

    while os.path.basename(path) != topLevelDir:
        path = os.path.dirname(path)

    return os.path.join(path, 'config.ini')
