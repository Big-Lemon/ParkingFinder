import functools
import httplib
from clay import config
from tornado.gen import coroutine

logger = config.get_logger('error')


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


class Timeout(BaseError):
    """
    Timeout Exception
    """
    error = "Timeout Exception"


def with_exception_handler(f):

    @coroutine
    @functools.wraps(f)
    def wrapper(self, *args, **params):
        # TODO validate self == Tornado Request
        # TODO move this to handlers.base directory
        try:
            yield f(self, *args, **params)

        except Timeout as ex:
            self.set_status(httplib.REQUEST_TIMEOUT)
            logger.error({
                "request": self.request,
                "body": self.request.body,
                "exception": ex

            })
            self.write({
                "error": "Request Expired",
                "exception": str(ex)
            })
        except (AssertionError, InvalidArguments, InvalidEntity) as ex:
            logger.warn({
                "request": self.request,
                "body": self.request.body,
                "exception": ex

            })
            self.set_status(httplib.BAD_REQUEST)
            self.write({
                "error": "Bad Request",
                "exception": str(ex)
            })
        except NotFound as ex:
            logger.warn({
                "request": self.request,
                "body": self.request.body,
                "exception": ex

            })
            self.set_status(httplib.NOT_FOUND)
            self.write({
                "error": "Not Found",
                "exception": str(ex)
            })
        except Unauthorized as ex:
            logger.warn({
                "request": self.request,
                "body": self.request.body,
                "exception": ex

            })
            self.set_status(httplib.NOT_FOUND)
            self.set_status(httplib.UNAUTHORIZED)
            self.write({
                "error": "Unauthorized",
                "exception": str(ex)
            })
        except Exception as ex:
            logger.error({
                "request": self.request,
                "body": self.request.body,
                "exception": ex
            })
            self.set_status(httplib.INTERNAL_SERVER_ERROR)
            self.write({
                "error": str(ex)
            })

    return wrapper
