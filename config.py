import configparser
import os

config = configparser.ConfigParser()

whitelisted = False
WHITELIST = [] # ['bot-stuff', 'foodifier', 'menu', 'bot-commands'] # bot will only run if message is in whitelisted channel (these are specific to my test server)
blacklisted = False
BLACKLIST = []


with open('token.txt', 'r') as f: # if running this yourself, create a bot token and put it in token.txt (purpose is so i can share this program without sharing my token)
    TOKEN = f.read().strip()


def read_config(filename = 'config.ini'):
    if not os.path.exists(filename):
        print('Config file does not exist! Creating new file...')
        reset_config(filename)
        return False
    global config, whitelisted, WHITELIST, blacklisted, BLACKLIST

    config.read(filename)

    whitelisted = config.get('Blocklist', 'whitelisted')
    blacklisted = config.get('Blocklist', 'blacklisted')
    WHITELIST = config.get('Blocklist', 'WHITELIST').split(',')
    BLACKLIST = config.get('Blocklist', 'BLACKLIST').split(',')
    return True

def write_config(filename = 'config.ini'):

    config['Blocklist'] = {'whitelisted':str(whitelisted), 
                            'blacklisted':str(blacklisted),
                            'WHITELIST':','.join(WHITELIST),
                            'BLACKLIST':','.join(BLACKLIST)}

    with open(filename, 'w') as f:
        config.write(f)

def reset_config(filename = 'config.ini'):

    with open(filename, 'w') as f:
        
        config = configparser.ConfigParser()
        config['Blocklist'] = {'whitelisted':'False', 
                            'blacklisted':'False',
                            'WHITELIST':'',
                            'BLACKLIST':''}  # Set whitelist and blacklist to empty list
        config.write(f)