from unittest import TestCase

from dreambuilder.packager import service


class PackagerServiceTest(TestCase):
    def test_options(self):
        """
        The option parser requires '--endpoint' and '--debug' option parsing.
        """
        o = service.Options()

        self.assertEquals(o['endpoint'], 'tcp:8000')
        o.parseOptions(["--endpoint=tcp:80"])
        self.assertEquals(o['endpoint'], 'tcp:80')

        self.failIf(o['debug'])
        o.parseOptions(["--debug"])
        self.failUnless(o['debug'])

    def test_factory(self):
        """
        Check that the debug flag is set properly in ExampleFactory.
        """
        f = service.ExampleFactory()
        self.failIf(f.debug)

        f = service.ExampleFactory(True)
        self.failUnless(f.debug)

    def test_makeService(self):
        """
        Check that makeService returns services that have the right information
        in them.
        """

        ms = service.makeService({'debug':False, 'endpoint':'tcp:1234'})

        example_server = ms.getServiceNamed('Example Server')
        self.failIf(example_server.factory.debug)
        self.assertEquals(example_server.endpoint._port, 1234)

        setup_service = ms.getServiceNamed('Setup Service')

        self.failUnless(isinstance(setup_service, service.SetupService))

    def test_startSetupService(self):
        """
        When setupservice is started, it will set up a callLater. Verify this
        behaviour.
        """
        class MockReactor:
            def __init__(self):
                self.calls = []

            def callLater(self, time, *args):
                self.calls.append((time, args))

        mockReactor = MockReactor()
        s = service.SetupService(mockReactor)

        self.assertEqual(mockReactor.calls, [])
        s.startService()

        self.assertEqual(mockReactor.calls, [(3, (s.done,))])
