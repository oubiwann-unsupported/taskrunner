from twisted.internet import reactor
from twisted.python import log

from dreambuilder import exceptions


def initialize(config):
    # create base and install dirs
    # install dependencies
    pass


def _install_lp_repo(uri, name, config):
    log.msg("Installing Launchpad repo %s from %s ..." % (name, url))
    return ["ls /dev/null"]


def _install_git_repo(uri, name, config):
    log.msg("Installing Git repo %s from %s ..." % (name, url))
    return ["ls /dev/null"]


def install_repos(config, just_lp=False, just_git=False):
    commands = []
    for uri, name in config.get_upstream_repos():
        if not just_git and uri.startswith("lp"):
            commands.extend(_install_lp_repo(uri, name, config))
        elif not just_lp and uri.startswith('git'):
            commands.extend(_install_git_repo(uri, name, config))
    return commands


def install_lp_repos(config):
    return install_repos(config, just_lp=True)


def install_git_repos(config):
    return install_repos(config, just_git=True)


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
    def __init__(self, factory, verb, obj):
        try:
            command_group = command_mapper[verb]
        except KeyError:
            raise exceptions.UnknownVerbParameter(verb)
        try:
            command_function = command_group[obj]
        except KeyError:
            raise exceptions.UnknownObjectParameter(obj)
        commands = command_function(factory.config)
        for command in commands:
            factory.run(command)
