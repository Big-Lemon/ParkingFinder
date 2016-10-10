class BaseError(Exception):
    pass


class AuthorizationError(BaseError):
    """
    Invalid Access Token Exception

    """
    error = 'Invalid Access Token'


class NotFound(BaseError):
    """
    Generic Not Found Exception
    """
    error = 'Not Found Exception'


class InvalidArguments(BaseError):
    """
    Invalid Argument
    """
    error = 'Invalid Arguments'
