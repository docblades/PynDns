"""
PynDns - Data persistence
"""
import json, sqlite3, logging

logger = logging.getLogger(__name__)

class InvalidConfiguration(Exception):
    def __init__(self, config):
        self.missing = []
        if not config.hostname:
            self.missing.append("hostname")
        if not config.username:
            self.missing.append("username")
        if not config.password:
            self.missing.append("password")
        self.message = "Config missing requirements: {0}".format(self.missing)
            
class Config(object):
    hostname = None
    username = None
    password = None

    def from_args(self, args):
        if args.hostname:
            self.hostname = args.hostname
        if args.username:
            self.username = args.username
        if args.password:
            self.password = args.password

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
        self.validate()

    def from_json(self, json_string):
        me_dict = json.loads(json_string)
        self.from_dict(me_dict)

    def from_file(self, config_file):
        me_dict = json.load(config_file)
        self.from_dict(me_dict)

    def validate(self):
        if self.hostname and self.username and self.password:
            return True
        else:
            raise InvalidConfiguration(self)

    def __str__(self):
        return "Config for {0}@{1}".format(self.username, self.hostname)

    def __repr__(self):
        return "<Config(hostname: {0}, username: {1})>".format(self.hostname, self.username)
