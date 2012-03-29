class Error(Exception):
    pass


class UnknownParameter(Error):
    pass


class UnknownVerbParameter(UnknownParameter):
    pass


class UnknownObjectParameter(UnknownParameter):
    pass
