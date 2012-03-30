class ProcessDispatcher(object):
    """
    """
    def __init__(self, config, command_mapper, commands):
        self.config = config
        self.debug = config.debug
        self.verb = self.config.options["verb"]
        self.obj = self.config.options["object"]
        self.command_mapper = command_mapper
        self.commands = commands
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
            command_group = self.command_mapper[self.verb]
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

