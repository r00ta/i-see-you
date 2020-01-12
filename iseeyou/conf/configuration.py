import json

class Configuration:
    def __init__(self, appsettings_path):
        conf = json.loads(open(appsettings_path, 'r').read())
        self.home_logs = conf['home_logs']
        self.account_name = conf['account_name']
        self.account_key = conf['account_key']
        self.container_name = conf['container_name']
        self.display_video = conf['display_video']
