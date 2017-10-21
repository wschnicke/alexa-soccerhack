# example of how to create and write to a config file
import configparser
config = configparser.ConfigParser()
config['DEFAULT'] = {'ScoresApiKey' :'Aaaaaaaaaaaaaaaaaaaaaaaaa'}
with open('config.ini', 'w') as configfile:
    config.write(configfile)
