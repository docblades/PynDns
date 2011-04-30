import unittest2
from pyndns import data
from StringIO import StringIO

class ConfigJSONTests(unittest2.TestCase):

    def setUp(self):
        self.config = data.Config()

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

class ConfigToJSON(ConfigJSONTests):
    def runTest(self):
        self.config.hostname = "testhost2"
        self.config.username = "testuser2"
        self.config.password = "testpass2"

        result = self.config.dump_to_json()

        self.assertIsNotNone(result)
        self.assertRegexpMatches(result, "\"username\"\s?:\s?\"testuser2\"")
        self.assertRegexpMatches(result, "\"hostname\"\s?:\s?\"testhost2\"")
        self.assertRegexpMatches(result, "\"password\"\s?:\s?\"testpass2\"")

class ConfigFromJSON(ConfigJSONTests):
    def runTest(self):
        testJSON = """{"hostname": "testhost3", "username": "testuser3", "password": "testpass3"}"""
        
        self.config.from_json(testJSON)

        self.assertEqual("testhost3", self.config.hostname)
        self.assertEqual("testuser3", self.config.username)
        self.assertEqual("testpass3", self.config.password)

class ConfigFromFile(ConfigJSONTests):
    def runTest(self):
        testJSON = """{"hostname": "testhost4", "username": "testuser4", "password": "testpass4"}"""

        fakeFile = StringIO(testJSON)

        self.config.from_file(fakeFile)

        self.assertEqual("testhost4", self.config.hostname)
        self.assertEqual("testuser4", self.config.username)
        self.assertEqual("testpass4", self.config.password)

class Config_Repr(ConfigJSONTests):
    def runTest(self):
        self.config.hostname = "testhost5"
        self.config.username = "testuser5"

        self.assertIn("hostname: testhost5", repr(self.config))
        self.assertIn("username: testuser5", repr(self.config))

class Config_Str(ConfigJSONTests):
    def runTest(self):
        self.config.hostname = "testhost6"
        self.config.username = "testuser6"

        self.assertIn("testuser6@testhost6", str(self.config))

class ConfigValidate_ReturnsTrueWhenRequiredValuesNotEmpty(ConfigJSONTests):
    def runTest(self):
        self.config.hostname = "testhost7"
        self.config.username = "username7"
        self.config.password = "password7"

        self.assertTrue(self.config.validate())
            
class ConfigValidate_RaisesExceptionWhenRequiredValuesEmpty(ConfigJSONTests):
    def runTest(self):
        self.config.hostname = "testhost8"
        self.config.username = "testuser8"

        with self.assertRaises(data.InvalidConfiguration) as context:
            self.config.validate()

        
