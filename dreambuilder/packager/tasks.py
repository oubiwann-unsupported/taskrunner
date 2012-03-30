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
