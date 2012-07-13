import os

from twisted.internet import defer, reactor, utils
from twisted.python import log

from dreambuilder import exceptions


class ProcessParallelizer(object):
    """
    This class takes one or more commands (potentially nested) in the form of
    a CommandExpression instance and converts each of these commands into
    deferreds, and converts groups of them into deferred lists.

    The rules are as follows:

    1) for each node in the expression, call utils.getProcessOutputAndValue and
       add general errbacks/callbacks for them
    2) if a node has siblings, gather their deferreds (returned from
       getProcessOutputAndValue), and put them in a deferred list
       and add general errbacks/callbacks for them
    3) for each nested command, ensure that it gets its deferred created in a
       callback of the current node's deferred
    4) if any of the nodes should halt on fail, add that specific errback to
       its deferred
    """
    def __init__(self, command_expression):
        self.commands = command_expression

    def callback(self, *args):
        log.msg("in callback: %s" % str(args))

    def errback(self, failure):
        log.msg("ERROR: %s" % failure)

    def halt(self, ignore):
        reactor.stop()

    def get_deferreds(self, commands=None):
        if not commands:
            commands = self.commands
        deferreds = []
        for command_exp in commands.walk():
            print ""
            print command_exp
            print command_exp.command
            args = command_exp.command.split()
            executable = args[0]
            deferred = utils.getProcessOutputAndValue(
                executable, args=args[1:], env=os.environ)
            deferred.addErrback(self.errback)
            if command_exp.halt_on_fail:
                deferred.addCallback(self.halt)
            deferred.addCallback(self.callback)
            deferred.addErrback(self.errback)
            deferreds.append(deferred)
        return defer.DeferredList(deferreds)


class ProcessDispatcher(object):
    """
    """
    def __init__(self, config, command_mapper):
        self.config = config
        self.debug = config.debug
        self.verb = self.config.options["verb"]
        self.obj = self.config.options["object"]
        self.command_mapper = command_mapper
        self.dispatch()

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
            command_group = self.command_mapper[self.verb]
        except KeyError:
            raise exceptions.UnknownVerbParameter(self.verb)
        try:
            command_function = command_group[self.obj]
            if self.debug:
                log.msg("this is the command function: %s" % command_function)
        except KeyError:
            raise exceptions.UnknownObjectParameter(self.obj)
        return ProcessParallelizer(command_function).get_deferreds()

    def start(self):
        deferred = self.runCommands(initialize(self.config))
        deferred.addErrback(self.errback)
        deferred.addCallback(self.dispatch)
        deferred.addErrback(self.errback)
        deferred.addCallback(self.finish)

