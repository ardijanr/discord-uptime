import json

def updateCFG():
    with open('servers.json') as f:
        servers = json.load(f)

    with open('config.json') as f:
        config = json.load(f)

    return servers, config

servers, config = updateCFG()


