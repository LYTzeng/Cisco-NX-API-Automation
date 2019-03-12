"""Custom exceptions"""

class CustomException(Exception):
    """The base class of all custom exceptions"""
    pass


class NoPrevRequestError(CustomException):
    """Raised when NX-API hasn't been called."""
    pass


class HttpError(CustomException):
    """Raised when HTTP response code != 200."""
    pass


class FuncInputError(CustomException):
    """Raised when the input param is in the wrong format"""
    pass