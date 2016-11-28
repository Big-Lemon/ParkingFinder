from contextlib import contextmanager
from tornado.gen import Return, coroutine

from ParkingFinder.base import Session


@contextmanager
def create_session():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except Return:
        session.commit()
        raise
    except:
        session.rollback()
        raise



def with_session(method):
    """
    Decorator that create a scoped session(transaction). this decorator
    will commit at the end, if any exception has thrown from inner function
    the transaction will rollback

    :param method:
    :return:
    """
    @coroutine
    def wrapper(*args, **params):
        _session = Session()
        try:
            result = yield method(session=_session, *args, **params)
            raise Return(result)
        except Return:
            _session.commit()
            raise
        except:
            _session.rollback()
            raise

    return wrapper
