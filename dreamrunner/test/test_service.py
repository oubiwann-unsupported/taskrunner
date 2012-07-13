from twisted.trial import unittest

from dreamrunner import service
from dreamrunner.config import Configuration


class OptionsTestCase(unittest.TestCase):
    """
    """
    def test_options_without_debug(self):
        """
        The option parser requires '--debug' option as well as 'verb' and
        'object' argument parsing.
        """
        o = service.Options()

        o.parseOptions(["install", "repos"])
        self.failIf(o["debug"])
        self.failUnless(o["verb"])
        self.failUnless(o["object"])
        self.assertEqual(o["verb"], "install")
        self.assertEqual(o["object"], "repos")

    def test_options_with_debug(self):
        """
        The option parser requires '--debug' option as well as 'verb' and
        'object' argument parsing.
        """
        o = service.Options()

        self.failIf(o["debug"])
        o.parseOptions(["--debug", "install", "repos"])
        self.failUnless(o["debug"])
        self.failUnless(o["verb"])
        self.failUnless(o["object"])
        self.assertEqual(o["verb"], "install")
        self.assertEqual(o["object"], "repos")


class ConfigurationServiceTestCase(unittest.TestCase):
    """
    """
    def test_startConfigurationService(self):
        """
        When setupservice is started, it will set up a callLater. Verify this
        behaviour.
        """
        config = Configuration(None, "../config.yaml")
        config.debug = False
        config_service = service.ConfigurationService(config)
        self.assertTrue(hasattr(config_service, "config"))
        self.assertEqual(config_service.config.debug, False)
