from twisted.internet import reactor
from twisted.python import log

from dreamrunner import service
from dreamrunner.config import Configuration
from dreamrunner.packager import tasks
from dreamrunner.processmanager import dispatcher
from dreamrunner.service import Options


class PackagerService(service.ConfigurationService):

    name = 'Packager Service'

    def getStartCallable(self):
        """
        """
        package_dispatcher = dispatcher.ProcessDispatcher(
            self.config, tasks.get_command_mapper(self.config))
        return package_dispatcher.dispatch

    def startService(self):
        """
        """
        log.msg("Starting PackagerService ...")
        reactor.callWhenRunning(self.getStartCallable())


def makeService(options, config_file=""):
    """
    """
    config = Configuration(options, filename=config_file)
    config.debug = options["debug"]
    packager_service = PackagerService(config)
    top_level_service = service.ServiceManager()
    packager_service.setServiceParent(top_level_service)
    return top_level_service
