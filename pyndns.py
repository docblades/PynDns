"""
PynDns - A Python DynDns client
Written By: Christian Blades (christian DOT blades AT docblades DOT com)
April 25 2011
"""

import logging, argparse, os, data, net
from argparse import ArgumentParser, FileType

VERSION = "PynDns 1.0"
logger = logging.getLogger(__name__)
DEFAULT_CONFIG_PATHS = ["~/.pyndns.conf", "~/.pyndns/pyndns.con", "/etc/pyndns.conf"]

class NoConfiguration(Exception):
    pass

def find_config_file(): #pragma: no cover
    for path in DEFAULT_CONFIG_PATHS:
        if os.path.exists(path):
            fp = open(path, "r")
            return fp
    return None

def build_parser():
    parser = ArgumentParser(description='A dyndns update client',
                            epilog='* Will override the config file')
    parser.add_argument('--version', action='version', version=VERSION)
    parser.add_argument('--config', metavar='FILE', nargs=1,
                        type=FileType('r'), default=None,
                        help='Specify which file to use for configuration')
    parser.add_argument('--hostname', default=None,
                        help='Which hostname to update*')
    parser.add_argument('--username', default=None,
                        help='DynDns username*')
    parser.add_argument('--password', default=None,
                        help='DynDns password*')
    parser.add_argument('--force-update', action='store_true', default=False,
                        help='Send update request, even if the IP has not changed.')
    return parser

def get_args(): #pragma: no cover
    parser = build_parser()
    args = parser.parse_args()
    return args

def build_config(args):
    config = data.Config()

    if args.config:
        fp = args.config
    else: #pragma: no cover
        fp = find_config_file()

    if fp:
        try:
            config.from_file(fp)
        except data.InvalidConfiguration as ex:
            logger.warn(ex.message)

    config.from_args(args)
    config.validate()
    return config

def do_update(config): #pragma: no cover
    request = net.DynDnsRequester(config.username, config.password)
    success = request.update_ip(net.get_ip_from_dyndns())
    codes = dict(map(lambda a, b: (a, b), request.codes, request.messages))
    return success, codes

if __name__ == "__main__": #pragma: no cover
    args = get_args()
    config = build_config(args)
    if net.has_ip_changed(config.hostname):
        print "IP for {0} has changed. Sending update.".format(config.hostname)
        resp = do_update(config)
    elif args.force-update:
        print "IP for {0} has not changed. Sending update anyway
    (force-update)".format(config.hostname)
        resp = do_update(config)
    else:
        print "IP for {0} has not changed. Exiting.".format(config.hostname)
        return

    if resp[0]:
        print "Successfully updated IP for {0}".format(config.hostname)
    else:
        print "A problem occurred while updating."

    for code in resp[1]:
        print "{0}: {1}".format(message, resp[1][code])
        
