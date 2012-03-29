from twisted.application import service, internet
from twisted.internet import endpoints, reactor
from twisted.python import log
from twisted.python import usage

from dreambuilder.config import Configuration
from dreambuilder.packager import tasks


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
    optFlags = [[
        'debug', 'd', 'Emit debug messages']]
    #optParameters = [[
    #    "endpoint", "s", DEFAULT_STRPORT,
    #    "string endpoint descriptiont to listen on, defaults to 'tcp:80'"]]

    def parseArgs(self, verb, obj):
        self['verb'] = verb
        self['object'] = obj


class SetupService(service.Service):
    name = 'Setup Service'

    def __init__(self, config):
        self.config = config

    def startService(self):
        """
        Custom initialisation code goes here.
        """
        log.msg("Retriculating Splines ...")
        reactor.callWhenRunning(tasks.TaskDispatcher(self.config).dispatch)

    def done(self):
        log.msg("Finished retriculating splines")


def makeService(options):
    """
    Generate and return a definition for all the services that this package
    needs to run. Will return a 'MultiService' object with two children.
    One is a ExampleFactory listening on the configured endpoint, and the
    other is an example custom Service that will do some set-up.
    """
    config = Configuration(options)
    config.debug = options["debug"]
    #f = protocols.ProcessFactory(config=config)
    #endpoint = endpoints.serverFromString(
    #    reactor, config.get_endpoint(type="unix"))
    #server_service = internet.StreamServerEndpointService(endpoint, f)
    #server_service.setName('Packager Service')

    setup_service = SetupService(config)

    top_level_service = service.MultiService()
    #server_service.setServiceParent(top_level_service)
    setup_service.setServiceParent(top_level_service)

    return top_level_service
