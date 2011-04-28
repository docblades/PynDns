import unittest2
from pyndns import net
from pyndns import URL_UPDATE
from urlparse import urlparse, parse_qs

class DynDnsRequestTestBase(unittest2.TestCase):
    def setUp(self):
    self.requester = net.DynDnsRequester("testuser", "testpass")

class DynDnsRequest_BuildUrl(DynDnsRequestTestBase):
    def runTest(self):
        result = self.requester.build_url("testhost", "10.0.0.1")

        parse_result = urlparse(result)

        dyndns_loc = urlparse(URL_UPDATE)

        

        self.assertEquals("https", parse_result.scheme)
        self.assertEquals("", parse_result.netloc)
        
