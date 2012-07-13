from twisted.trial import unittest

from dreamrunner.processmanager import protocols


class ExampleProtocolTestCase(unittest.TestCase):
    """
    """


class ExampleFactoryTestCase(unittest.TestCase):
    """
    """
    def test_factory(self):
        """
        Check that the debug flag is set properly in ExampleFactory.
        """
        f = protocols.ExampleFactory()
        self.failIf(f.debug)

        f = protocols.ExampleFactory(True)
        self.failUnless(f.debug)


class ProcessProtocolTestCase(unittest.TestCase):
    """
    """


class ProcessFactoryTestCase(unittest.TestCase):
    """
    """
