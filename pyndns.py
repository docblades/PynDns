"""
PynDns - A Python DynDns client
Written By: Christian Blades (christian DOT blades AT docblades DOT com)
April 25 2011
"""

import urllib2, re, json
from BeautifulSoup import BeautifulSoup

def get_ip_from_dyndns():
    url = "http://checkip.dyndns.com"
    response = urllib2.urlopen(url)
    page = BeautifulSoup(response)
    ip_match = re.match("Current IP Address: (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", page.body.text)
    ip_addr = ip_match.group(1)
    return ip_addr

if __name__ == "__main__":
    config = data.Config()
    
    
