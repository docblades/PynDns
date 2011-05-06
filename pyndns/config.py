'''
PynDns - Global configuration
'''

import logging, os

logger = logging.getLogger('PynDns')
if os.getenv('PYNDNS_DEBUG'):
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.FileHandler("./pyndns_log.txt", mode='a+'))
