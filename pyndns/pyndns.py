"""
PynDns - A Python DynDns client
Written By: Christian Blades (christian DOT blades AT docblades DOT com)
April 25 2011
"""

import logging, argparse, os, data, net, sys
from config import logger
from argparse import ArgumentParser, FileType

HOME = os.getenv('HOME', '')
VERSION = "PynDns 1.0"
DEFAULT_CONFIG_PATHS = [os.path.join(HOME, ".pyndns.conf"), os.path.join(HOME, '.pyndns', 'pyndns.conf'), "/etc/pyndns.conf"]

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
    parser.add_argument('--force', action='store_true', default=False,
                        help='Send update request, even if the IP has not changed.')
    return parser

def get_args(): #pragma: no cover
    parser = build_parser()
    args = parser.parse_args()
    return args

def build_config(args):
    config = data.Config()

    if args.config:
        logger.debug('Loading file from --config')
        fp = args.config
    else: #pragma: no cover
        logger.debug('Looking for a config file')
        fp = find_config_file()

    if fp:
        logger.debug('Found a config file. Loading.')
        try:
            config.from_file(fp)
        except data.InvalidConfiguration as ex:
            logger.warn(ex.message)

    logger.debug('Overwriting config params with command line args.')
    config.from_args(args)
    logger.debug('Running validation against config')
    config.validate()
    return config

def do_update(config): #pragma: no cover
    request = net.DynDnsRequester(config.username, config.password)
    success = request.update_ip(config.hostname, net.get_ip_from_dyndns())
    codes = dict(map(lambda a, b: (a, b), request.codes, request.messages))
    return success, codes

def main():
    args = get_args()
    config = build_config(args)
    if net.has_ip_changed(config.hostname):
        print "IP for {0} has changed. Sending update.".format(config.hostname)
        resp = do_update(config)
    elif args.force:
        print "IP for {0} has not changed. Sending update anyway (force-update)".format(config.hostname)
        resp = do_update(config)
    else:
        print "IP for {0} has not changed. Exiting.".format(config.hostname)
        return 0

    if resp[0]:
        print "Successfully updated IP for {0}".format(config.hostname)
        return 0
    else:
        print "A problem occurred while updating."
        for code in resp[1]:
            print "{0}: {1}".format(message, resp[1][code])
            return 1

if __name__ == "__main__": #pragma: no cover
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.FileHandler("./log.txt", mode='a+'))
    sys.exit(main())
