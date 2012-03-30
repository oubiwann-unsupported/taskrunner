from dreambuilder import exceptions


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
        self.children = []
        self.check_args(args)
        self.check_children()

    def check_args(self, args):
        nested_index = 1
        if not args:
            return
        first_arg = args[0]
        if first_arg and isinstance(first_arg, basestring):
            if self.command:
                raise exceptions.MultipleCommandsError()
            self.command = first_arg
        elif isinstance(first_arg, CommandExpression):
            nested_index = 0
        # now that we know where the nested commands start, we can set the
        # children
        self.children = args[nested_index:]

    def check_children(self):
        for child in self.children:
            if isinstance(child, basestring):
                raise exceptions.MultipleCommandsError()
