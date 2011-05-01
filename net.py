"""
PynDns network objects
"""
import urllib2, pyndns, re
from urllib import urlencode
from dnslib import socket
from BeautifulSoup import BeautifulSoup
import pickle
import logging

logger = logging.getLogger(__name__)

URL_UPDATE = "https://members.dyndns.org:443/nic/update"
URL_LIST = [URL_UPDATE]

def has_ip_changed(hostname): #pragma: no cover
    dns_ip = get_ip_by_dns(hostname)
    this_ip = get_ip_from_dyndns()
    return this_ip.strip() != dns_ip.strip()

def get_ip_by_dns(hostname): #pragma: no cover
    return socket.gethostbyname(hostname)

def get_ip_from_dyndns(): #pragma: no cover
    url = "http://checkip.dyndns.com"
    response = urllib2.urlopen(url)
    page = BeautifulSoup(response)
    ip_match = re.match("Current IP Address: (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", page.body.text)
    ip_addr = ip_match.group(1)
    return ip_addr

class DynDnsResponseException(Exception):
    def __init__(self, code, message):
        self.message = "{0}: {1}".format(code, message)
        self.code = code

class DynDnsRequester(object):
    opener = None
    success = None
    codes = []
    messages = []

    RESPONSE_CODES = {
        # Account-Related Errors
        "badauth": "The username and password pair do not match a real user.",
        "!donator": "An option available only to credited users (such as offline URL) was specified, but the user is not a credited user. If multiple hosts were specified, only a single !donator will be returned.",
        # Update Complete
        "good": """The update was successful, and the hostname is now updated.""",
        "nochg": """The update changed no settings, and is considered abusive. Additional nochg updates will cause the hostname to become blocked.""",
        # Hostname-Related Errors
        "notfqdn": """The hostname specified is not a fully-qualified domain name (not in the form hostname.dyndns.org or domain.com).""",
        "nohost": "The hostname specified does not exist in this user account (or is not in the service specified in the system parameter)",
        "numhost": """Too many hosts (more than 20) specified in an update. Also returned if trying to update a round robin (which is not allowed)""",
        # Agent-Related Errors
        "abuse": """The hostname specified is blocked for update abuse.""",
        "badagent": """The user agent was not sent or HTTP method is not permitted (we recommend use of GET request method).""",
        "good 127.0.0.1": """This answer indicates good update only when 127.0.0.1 address is requested by update. In all other cases it warns user that request was ignored because of agent that does not follow our specifications.""",
        # Service Errors
        "dnserr": "DNS error encountered",
        "911": "There is a problem or scheduled maintenance on our side."}
    
    def __init__(self, username, password):
        self.opener = self.build_opener(username, password)
        logger.info("New DynDnsRequester for user: '{0}'".format(username))

    def build_opener(self, username, password):
        pass_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
        pass_mgr.add_password(None, URL_LIST, username, password)

        handler = urllib2.HTTPBasicAuthHandler(pass_mgr)
        opener = urllib2.build_opener(handler)

        return opener

    def build_url(self, hostname, ipaddr):
        qstring = urlencode({"hostname": hostname,
                             "myip": ipaddr,
                             "wildcard": "NOCHG",
                             "mx": "NOCHG",
                             "backmx": "NOCHG"})
        upd_url = "%(url)s?%(qstring)s" % {"url": URL_UPDATE,
                                         "qstring": qstring}
        logger.debug("Built url: {0}".format(upd_url))
        return upd_url

    def update_ip(self, hostname, ipaddr): #pragma: no cover
        upd_url = self.build_url(hostname, ipaddr)
        response = self.opener.open(upd_url)
        self.success = self.validate_response(response)
        return self.success

    def validate_response(self, response):
        codes = self.parse_response(response)
        error_codes = ['badauth', '!donator', 'notfqdn',
                       'nohost', 'numhost', 'abuse',
                       'badagent', 'good 127.0.0.1']
        warn_codes = ['dnserr', '911', 'nochg']
        
        for code in codes:
            if code in error_codes:
                logger.error("Response from DynDns: '{0}'".format(code))
                raise DynDnsResponseException(code, self.get_message_from_code(code))
            elif code in warn_codes:
                logger.warn("Response from DynDns: '{0}'".format(code))
                return False

        return True
        
    def get_message_from_code(self, code):
        if code in self.RESPONSE_CODES:
            return self.RESPONSE_CODES[code]
        else:
            return str()
    
    def parse_response(self, response):
        self.codes = []
        for code in response:
            self.codes.append(code.strip())

        return self.codes
