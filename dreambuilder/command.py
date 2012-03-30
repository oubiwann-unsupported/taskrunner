class SExpression(list):
    """
    """


class CommandExpression(SExpression):
    """
    """
    def __init__(self, *args, **kwargs):
                 #command="", halt_on_fail=False, message="", skip=False,
                 #*args):
        self.command = kwargs.get("command") or ""
        self.halt_on_fail = kwargs.get("halt_on_fail") or False
        self.message = kwargs.get("message") or ""
        self.skip = kwargs.get("skip") or False
        if not self.command and isinstance(args[0], basestring):
            self.command = args[0]
