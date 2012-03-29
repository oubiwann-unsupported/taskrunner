import re

from twisted.internet import protocol
from twisted.internet import reactor

from dreambuilder.packager import tasks


class ExampleProtocol(protocol.Protocol):
    """
    Your protocol would replace this placeholder.
    """


class ExampleFactory(protocol.ServerFactory):
    """
    Your factory would replace this placeholder. Note that there is a debug
    option passed to __init__, this comes from the commandline when the command
    "twistd example --debug" is used.
    """
    protocol = ExampleProtocol

    def __init__(self, debug=False):
        self.debug = debug

    def connectionMade(self):
        """
        Small example of how to do switch on the debug flag.
        """
        if self.debug:
            log.msg("Connection Made")


class ProcessProtocol(protocol.ProcessProtocol):
    """
    """
    def __init__(self, verses):
        self.verses = verses
        self.data = ""

    def connectionMade(self):
        print "connectionMade!"
        for i in range(self.verses):
            self.transport.write("Aleph-null bottles of beer on the wall,\n" +
                                 "Aleph-null bottles of beer,\n" +
                                 "Take one down and pass it around,\n" +
                                 "Aleph-null bottles of beer on the wall.\n")
        self.transport.closeStdin() # tell them we're done

    def outReceived(self, data):
        print "outReceived! with %d bytes!" % len(data)
        self.data = self.data + data

    def errReceived(self, data):
        print "errReceived! with %d bytes!" % len(data)

    def inConnectionLost(self):
        print "inConnectionLost! stdin is closed! (we probably did it)"

    def outConnectionLost(self):
        print "outConnectionLost! The child closed their stdout!"
        # now is the time to examine what they wrote
        #print "I saw them write:", self.data
        (dummy, lines, words, chars, file) = re.split(r'\s+', self.data)
        print "I saw %s lines" % lines

    def errConnectionLost(self):
        print "errConnectionLost! The child closed their stderr."

    def processExited(self, reason):
        print "processExited, status %d" % (reason.value.exitCode,)

    def processEnded(self, reason):
        print "processEnded, status %d" % (reason.value.exitCode,)
        print "quitting"
        reactor.stop()


class ProcessFactory(protocol.ServerFactory):
    """
    """
    protocol = ProcessProtocol

    def __init__(self, config=None):
        self.config = config
        self.dispatch()

    def dispatch(self):
        verb = self.config.options["verb"]
        obj = self.config.options["object"]
        tasks.TaskDispatcher(self, verb, obj)

    def run(self, command):
        args = command.split()
        executable = args[0]
        reactor.spawnProcess(self.protocol, executable, args=args)

    def connectionMade(self):
        """
        Small example of how to do switch on the debug flag.
        """
        if self.debug:
            log.msg("Connection Made")
