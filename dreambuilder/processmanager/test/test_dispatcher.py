from twisted.internet import defer
from twisted.trial import unittest

from dreambuilder.command import CommandExpression as CExp
from dreambuilder.processmanager import dispatcher


def fake_getProcessOutputAndValue(executable, args, env={}):
    return defer.Deferred()    


class ProcessParallelizerTestCase(unittest.TestCase):
    """
    """
    def setUp(self):
        self.patch(
            dispatcher.utils, "getProcessOutputAndValue",
            fake_getProcessOutputAndValue)

    def test_command_as_deferred(self):
        command = CExp("Do this thing")

        
