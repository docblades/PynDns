"""
PynDns - A Python DynDns client
Written By: Christian Blades (christian DOT blades AT docblades DOT com)
April 25 2011
"""

import logging, argparse, os

logger = logging.getLogger(__name__)
DEFAULT_CONFIG_PATHS = ["~/.pyndns.conf", "~/.pyndns/pyndns.con", "/etc/pyndns.conf"]

class NoConfiguration(Exception):
    pass

def find_config(args):
    config = data.Config()

    for path in DEFAULT_CONFIG_PATHS:
        if os.path.exists(path):
            fp = open(path, "r")
            config.from_file(fp)
            fp.close()
            return config

def do_argparse():
    pass

if __name__ == "__main__":
    config = data.Config()
    
