import functools
import time

from tornado.gen import (
    Return,
    coroutine,
    sleep
)

from ParkingFinder.base.errors import BaseError


def with_repeat(timeout=None, repeat_times=None, repeat_exceptions=None, duration=None):
    """
    Decorator with_repeat, repeat wrapped function 'repeat_times' if the function
    raises exception which is a expected 'repeated_exceptions'

    :param int timeout: timeout in # seconds, default timeout is 300 seconds
    :param int repeat_times: maximum repeat times, repeat once if not define
    :param list<Exception> repeat_exceptions:
        repeat the wrapped method if the method throws a expected repeated_exceptions
    :param int duration: duration between each repeat

    :return func: wrapped function
    """

    def decorator(method):

        @functools.wraps(method)
        @coroutine
        def wrapper(*args, **params):

            _repeat_times = repeat_times
            _timeout = params.get('timeout', None) or timeout
            _start = time.time()
            _end = _start
            if _timeout:
                _end += _timeout
            exception = None

            while True:
                # max timeout constraint
                if _timeout and time.time() > _end:
                    raise Timeout(exception=exception)

                # max repeat constraint
                if _repeat_times != None and _repeat_times <= 0:
                    raise ReachRepeatLimit(exception=exception)

                if _repeat_times:
                    _repeat_times -= 1

                if duration:
                    yield sleep(duration=duration)

                try:
                    result = yield method(*args, **params)
                    raise Return(result)
                except Return:
                    raise
                except repeat_exceptions as ex:
                    exception = ex
                except Exception:
                    raise

        return wrapper

    return decorator


class Timeout(BaseError):
    """
    Timeout Exception
    """
    error = "Timeout Exception"


class ReachRepeatLimit(BaseError):
    """
    Timeout Exception
    """
    error = "Reach Repeat Limit"
