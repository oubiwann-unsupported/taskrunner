from twisted.application import service, internet
from twisted.internet import endpoints, protocol
from twisted.python import log
from twisted.python import usage


DEFAULT_STRPORT = 'tcp:8000'


class Options(usage.Options):
    """
    Provide a --debug option for starting the server in debug mode, and the
    ability to define what to listen on by using a string endpoint description.

    Documentation on how to configure a usage.Options object is provided here:
    http://twistedmatrix.com/documents/current/core/howto/options.html

    Endpoints are documented here in the API documentation:
    http://twistedmatrix.com/documents/current/api/twisted.internet.endpoints.html
    """
    optFlags = [['debug', 'd', 'Emit debug messages']]
    optParameters = [["endpoint", "s", DEFAULT_STRPORT,
                      "string endpoint descriptiont to listen on, defaults to 'tcp:80'"]]


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


class SetupService(service.Service):
    name = 'Setup Service'

    def __init__(self, reactor):
        self.reactor = reactor

    def startService(self):
        """
        Custom initialisation code goes here.
        """
        log.msg("Retriculating Splines")

        self.reactor.callLater(3, self.done)

    def done(self):
        log.msg("Finished retriculating splines")


def makeService(options):
    """
    Generate and return a definition for all the services that this package
    needs to run. Will return a 'MultiService' object with two children.
    One is a ExampleFactory listening on the configured endpoint, and the
    other is an example custom Service that will do some set-up.
    """
    from twisted.internet import reactor

    debug = options['debug']

    f = ExampleFactory(debug=debug)
    endpoint = endpoints.serverFromString(reactor, options['endpoint'])
    server_service = internet.StreamServerEndpointService(endpoint, f)
    server_service.setName('Example Server')

    setup_service = SetupService(reactor)

    ms = service.MultiService()
    server_service.setServiceParent(ms)
    setup_service.setServiceParent(ms)

    return ms
