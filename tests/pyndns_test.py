import unittest
from pyndns import pyndns

class ConfigJSONTests(unittest.TestCase):

    def setUp(self):
        self.config = pyndns.Config()

    def tearDown(self):
        self.config = None

class ConfigToDict(ConfigJSONTests):
    def runTest(self):
        self.config.hostname = "testhost"
        self.config.username = "testuser"
        self.config.password = "testpass"

        result = self.config.to_dict()

        self.assertEqual("testhost", result["hostname"])
        self.assertEqual("testuser", result["username"])
        self.assertEqual("testpass", result["password"])

    
