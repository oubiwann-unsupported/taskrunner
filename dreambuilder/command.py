from dreambuilder import exceptions


class CommandExpression(object):
    """
    """
    def __init__(self, *args, **kwargs):
        """
        To get the cleanest usage, with lots of flexibility on what can
        constitute a command, we need to not do named parameters, but rather
        extract those from extended call syntax.

        Args:
            command (str): If the first positional parameter is a string, it
                will be interpreted as a string.

            command (CommandExpression): If the first argument is a
                CommandExpression object, the remainder of the positional
                arguments must also be CommandExpression objects.

        Kwargs:
            command (str): A text string representing a command to be executed.

            halt_on_fail (bool): if True, and the command for this instance of
                CommandExpression or any nested instances of CommandExpression
                results in a failure, the program will be halted.

            message (str): A message to write to the log file when this
                instance of CommandExpression is eventually called.

            skip (bool): If True, this command will not be called.
        """
        self.command = ""
        self.halt_on_fail = False
        self.message = ""
        self.skip = False
        self.children = []
        self.parent = None
        self.parse_kwargs(kwargs)
        self.check_args(args)
        self.class_name = self.__class__.__name__

    def __repr__(self):
        return "<class %s '%s'>" % (self.class_name, self.command)

    def parse_kwargs(self, kwargs):
        self.command = kwargs.get("command") or ""
        self.halt_on_fail = kwargs.get("halt_on_fail") or False
        self.message = kwargs.get("message") or ""
        self.skip = kwargs.get("skip") or False

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
        self.check_children()

    def check_children(self):
        children = self.children[:]
        self.children = []
        for child in children:
            if isinstance(child, basestring):
                raise exceptions.MultipleCommandsError()
            elif True in [isinstance(child, x) for x in [set, list, tuple]]:
                self.children.extend(list(child))
            elif isinstance(child, CommandExpression):
                child.parent = self
                self.children.append(child)
            else:
                raise TypeError(
                    "Don't know how to handle child %s" % str(child))

    def has_children(self):
        # turning the list into a boolean
        return not not self.children

    def has_siblings(self):
        if not self.parent:
            return False
        if len(self.parent.children) > 1:
            return True
        return False

    def get_descendant(self, *indices):
        try:
            child = self.children[indices[0]]
        except IndexError:
            msg = "%s has no descendant at index 0 with value %s" % (
                self.class_name, indices[0],)
            raise exceptions.NoDescendantError(msg)
        for index_index, index_value in enumerate(indices[1:]):
            try:
                child = child.children[index_value]
            except IndexError:
                msg = "%s has no descendant at index %s with value %s" % (
                    self.class_name, index_index, index_value)
                raise exceptions.NoDescendantError(msg)
        return child

    def depth_first(self):
        """
        """
        stack = [self]
        while stack:
            current = stack.pop(0)
            yield current
            stack = current.children + stack

    def breadth_first(self):
        """
        """
        stack = [self]
        while stack:
            current = stack.pop(0)
            yield current
            stack.extend(current.children)

    def walk(self, type="depth"):
        """
        This is a depth-first search of the the expression for any nested
        expressions.
        """
        if type == "depth":
            return depth_first()
        elif type == "breadth":
            return breadthe_first()
