import json

class Configuration:
    def __init__(self, appsettings_path):
        conf = json.loads(open(appsettings_path, 'r').read())
        self.blob_connection_string = conf['blob_connection_string']
        self.container_name = conf['container_name']
        self.display_video = conf['display_video']
