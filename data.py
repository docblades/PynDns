"""
PynDns - Data persistence
"""
import json, sqlite3

class Config(object):
    hostname = None
    username = None
    password = None

    def to_dict(self):
        me_dict = {"hostname": self.hostname,
                   "username": self.username,
                   "password": self.password}
        return me_dict

    def dump_to_json(self):
        return json.dumps(self.to_dict())

    def from_dict(self, config_dict):
        self.hostname = config_dict["hostname"]
        self.username = config_dict["username"]
        self.password = config_dict["password"]

    def from_json(self, json_string):
        me_dict = json.loads(json_string)
        self.from_dict(me_dict)

    def from_file(self, config_file):
        me_dict = json.load(config_file)
        self.from_dict(me_dict)

    def __str__(self):
        return self.username + "@" + self.hostname

    def __repr__(self):
        return "<pydndns.Config object hostname:" + self.hostname + " username: " + self.username + ">"    
