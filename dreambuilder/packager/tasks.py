import os

from twisted.internet import defer, reactor, utils
from twisted.python import log

from dreambuilder import exceptions


def initialize(config):
    if config.debug:
        log.msg("Initializing installation ...")
    return [
        "sudo apt-get install -y %s" % config.pre_install_deps,
        "mkdir -p %s" % config.install_dir]


def _install_lp_repo(uri, name, config):
    if config.debug:
        log.msg("Installing Launchpad repo %s from %s ..." % (name, uri))
    return ["bzr branch %s %s" % (uri, os.path.join(config.install_dir, name))]


def _install_git_repo(uri, name, config):
    if config.debug:
        log.msg("Installing Git repo %s from %s ..." % (name, uri))
    return ["git clone %s %s" % (uri, os.path.join(config.install_dir, name))]


def install_repos(config, just_lp=False, just_git=False):
    commands = []
    for data in config.upstream_repos:
        uri = data["uri"]
        name = data["name"]
        if config.debug:
            print uri, name
        if not just_git and uri.startswith("lp"):
            commands.extend(_install_lp_repo(uri, name, config))
        elif not just_lp and uri.startswith('git'):
            commands.extend(_install_git_repo(uri, name, config))
    return commands


def install_lp_repos(config):
    return install_repos(config, just_lp=True)


def install_git_repos(config):
    return install_repos(config, just_git=True)


def finalize(config):
    if config.debug:
        log.msg("Running final commands ...")
    return ["chown -R %s %s" % (config.user, config.install_dir)]


command_mapper = {
    'install': {
        'lp-repos': install_lp_repos,
        'git-repos': install_git_repos,
        'repos': install_repos,
        },
    }


class TaskDispatcher(object):
    """
    """
    def __init__(self, config):
        self.config = config
        self.debug = config.debug
        self.verb = self.config.options["verb"]
        self.obj = self.config.options["object"]
        self.start()

    def callback(self, result, command):
        out, err, signalNum = result
        if err and signalNum != 0:
            self.errback("%s (signal number: %s)" % (err.strip(), signalNum))
        elif err:
            log.msg("Error? %s" % err)
        else:
            log.msg("The results of '%s'..." % command)
            log.msg(out.strip())

    def errback(self, failure):
        log.msg("ERROR: %s" % failure)

    def finish(self, result):
        deferred = self.runCommands(finalize(self.config))
        deferred.addErrback(self.errback)
        deferred.addCallback(lambda ign: reactor.stop())
        return deferred

    def run(self, command):
        args = command.split()
        executable = args[0]
        deferred = utils.getProcessOutputAndValue(
            executable, args=args[1:], env=os.environ)
        deferred.addCallback(self.callback, command)
        deferred.addErrback(self.errback)
        return deferred

    def runCommands(self, commands):
        if self.debug:
            log.msg("these are the commands: %s" % commands)
        deferreds = []
        for command in commands:
            deferred = self.run(command)
            deferred.addErrback(self.errback)
            deferreds.append(deferred)
        deferred_list = defer.DeferredList(deferreds)    
        return deferred_list

    def dispatch(self, results=None):
        if self.debug and results:
            log.msg("Start-up results: %s" % results)
        try:
            command_group = command_mapper[self.verb]
        except KeyError:
            raise exceptions.UnknownVerbParameter(self.verb)
        try:
            command_function = command_group[self.obj]
            if self.debug:
                log.msg("this is the command function: %s" % command_function)
        except KeyError:
            raise exceptions.UnknownObjectParameter(self.obj)
        deferred = defer.maybeDeferred(command_function, self.config)
        deferred.addErrback(self.errback)
        deferred.addCallback(self.runCommands)
        deferred.addErrback(self.errback)
        return deferred

    def start(self):
        deferred = self.runCommands(initialize(self.config))
        deferred.addErrback(self.errback)
        deferred.addCallback(self.dispatch)
        deferred.addErrback(self.errback)
        deferred.addCallback(self.finish)

