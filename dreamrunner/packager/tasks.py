import os

from twisted.internet import defer, reactor, utils
from twisted.python import log

from dreamrunner import exceptions
from dreamrunner.command import CommandExpression as CExp


class Tasks(object):
    """
    """
    def __init__(self, config):
        self.config = config
        self.pre_install_cexp = CExp(
            CExp("sudo apt-get install -y %s" % self.config.pre_install_deps),
            CExp("mkdir -p %s" % self.config.install_dir),
            message="Initializing installation ...",
            halt_on_fail=True
        )
        self.post_install_cexp = CExp(
            CExp("chown -R %s %s" % (config.user, config.install_dir)),
            message="Running final commands ..."
        )

    def build_repos_cexp(self, just_lp=False, just_git=False):
        commands = []
        for data in self.config.upstream_repos:
            uri = data["uri"]
            name = data["name"]
            if self.config.debug:
                log.msg("%s, %s" % (uri, name))
            if not just_git and uri.startswith("lp"):
                cexp = CExp(
                    "bzr branch %s %s" % (
                        uri, os.path.join(self.config.install_dir, name)),
                    message="Installing Launchpad repo %s from %s ..." % (
                        name, uri))
            elif not just_lp and uri.startswith('git'):
                cexp = CExp(
                    "git clone %s %s" % (
                        uri, os.path.join(self.config.install_dir, name)),
                    message="Installing Git repo %s from %s ..." % (
                        name, uri))
            commands.append(cexp)
        return commands


def complete_install(config):
    tasks = Tasks(config)
    return CExp(
        tasks.pre_install_cexp,
        tasks.build_repos_cexp(),
        tasks.post_install_cexp
    )


# This is used by the packager service so that the ProcessDispatcher can call
# the CommandExpression instance that is appropriate for the verb-object pair
# that was passed as arguments to twistd on the command line.
#
# Note that for the object keys, the corresponding value needs to be a
# callable.
def get_command_mapper(config):
    return {
    "install": {
        "deps": Tasks(config).pre_install_cexp,
        "repos": Tasks(config).build_repos_cexp,
        "all": complete_install(config),
    },
}
