from twisted.internet import defer
from twisted.trial import unittest

from dreamrunner.command import CommandExpression as CExp
from dreamrunner.processmanager import dispatcher


def fake_getProcessOutputAndValue(executable, args, env={}):
    return defer.succeed("Yay!")


class ProcessParallelizerTestCase(unittest.TestCase):
    """
    """
    def setUp(self):
        self.patch(
            dispatcher.utils, "getProcessOutputAndValue",
            fake_getProcessOutputAndValue)

    def test_command_as_deferred(self):

        def check(result):
            self.assertEqual(result, [(True, None)])

        commands = CExp("Do this thing")
        parallelizer = dispatcher.ProcessParallelizer(commands)
        deferreds = parallelizer.get_deferreds()
        deferreds.addCallback(check)
        return deferreds


class ProcessDispatcherTestCase(unittest.TestCase):
    """
    """
