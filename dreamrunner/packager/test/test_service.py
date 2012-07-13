from twisted.internet import defer, reactor
from twisted.trial import unittest

from dreambuilder.config import Configuration
from dreambuilder.packager import service, tasks


class PackagerServiceTestCase(unittest.TestCase):
    """
    """
    def test_makeService(self):
        """
        Check that makeService returns services that have the right information
        in them.
        """
        def fake_dispatch():
            print "Caling fake_dispatch ..."
            self.dispatch_called = True

        def fake_getStartCallable(ignored):
            print "calling fake_getStartCallable ..."
            return fake_dispatch

        self.patch(service.PackagerService, "getStartCallable", 
                   fake_getStartCallable)
        self.dispatch_called = False
        ms = service.makeService(
            {'debug': False, 'verb': 'install', 'object': 'repos'},
            "../config.yaml")
        packager_service = ms.getServiceNamed('Packager Service')
        packager_service.startService()
        self.failUnless(isinstance(packager_service, service.PackagerService))
        self.assertEqual(self.dispatch_called, True)
        packager_service.stopService()

    test_makeService.skip = "There's a bug with this test right now"
