from twisted.application import service
from twisted.python import usage


class Options(usage.Options):
    """
    """
    optFlags = [[
        'debug', 'd', 'Emit debug messages']]
    #optParameters = [[
    #    "endpoint", "s", DEFAULT_STRPORT,
    #    "string endpoint descriptiont to listen on, defaults to 'tcp:80'"]]

    def parseArgs(self, verb, obj):
        self['verb'] = verb
        self['object'] = obj


class ServiceManager(service.MultiService):
    
    name = "Service Manager"


class ConfigurationService(service.Service):

    name = "Configuration Service"

    def __init__(self, config):
        self.config = config
