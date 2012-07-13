class Error(Exception):
    """
    A base class for exceptions.
    """
    def __init__(self, msg=None):
        if msg == None:
            msg = self.__doc__.strip()
        super(Error, self).__init__(msg)


class UnknownParameter(Error):
    pass


class UnknownVerbParameter(UnknownParameter):
    pass


class UnknownObjectParameter(UnknownParameter):
    pass


class ExpressionError(Error):
    pass


class MultipleCommandsError(ExpressionError):
    """
    Only one string command per CommandExpression is permitted.
    """

class NoDescendantError(Error):
    pass
