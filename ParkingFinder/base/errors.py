class BaseError(Exception):

    error = None

    def __init__(self, **params):
        if not self.error:
            raise NotImplementedError
        self.params = params

    def __str__(self):
        load = {
            'error': self.error,
            'params': self.params
        }
        return str(load)


class Unauthorized(BaseError):
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


class InvalidEntity(BaseError):
    """
    Invalid Entity
    """
    error = "Entity construction is not consistent with the corresponding definition "
