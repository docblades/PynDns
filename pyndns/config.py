'''
PynDns - Global configuration
'''

import logging

logger = logging.getLogger('PynDns')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.FileHandler("./log.txt", mode='a+'))
