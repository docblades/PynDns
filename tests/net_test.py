import unittest2
from pyndns import net
from pyndns.net import URL_UPDATE
from urlparse import urlparse, parse_qs
import urllib2

class DynDnsRequestTestBase(unittest2.TestCase):
    def setUp(self):
        self.requester = net.DynDnsRequester("testuser", "testpass")

    def tearDown(self):
        self.requester = None

class DynDnsRequest_BuildUrl(DynDnsRequestTestBase):
    def runTest(self):
        result = self.requester.build_url("testhost", "10.0.0.1")

        parse_result = urlparse(result)
        query = parse_qs(parse_result.query)

        dyndns_loc = urlparse(URL_UPDATE).netloc
        # Values are in a list because of the way parse_qs works
        check_dict = {"hostname": ["testhost"],
                      "myip": ["10.0.0.1"],
                      "wildcard": ["NOCHG"],
                      "mx": ["NOCHG"],
                      "backmx": ["NOCHG"]}

        self.assertEquals("https", parse_result.scheme)
        self.assertEquals(dyndns_loc, parse_result.netloc)
        self.assertDictEqual(check_dict, query)

class DynDnsRequest_BuildOpener(DynDnsRequestTestBase):
    def runTest(self):
        """
        Todo: Write a better test
        """
        opnr = self.requester.build_opener("testuser1", "testpass1")
        self.assertEquals(opnr.__class__, urllib2.OpenerDirector)

class DynDnsRequest_ValidateResponse_GoodResponse(DynDnsRequestTestBase):
    def runTest(self):
        t_resp = ["good", "foo"]

        self.assertTrue(self.requester.validate_response(t_resp))

class DynDnsRequest_ValidateResponse_WarnResponse(DynDnsRequestTestBase):
    def runTest(self):
        t_resp = ["bar", "baz", "nochg", "foo"]
        
        self.assertFalse(self.requester.validate_response(t_resp))

class DynDnsRequest_ValidateResponse_ErrorResponse(DynDnsRequestTestBase):
    def runTest(self):
        t_resp = ["bar", "baz", "badauth", "nochg", "foo"]

        self.assertRaises(net.DynDnsResponseException, self.requester.validate_response, t_resp)
