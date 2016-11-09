from contextlib import contextmanager
from tornado.gen import Return, coroutine

from ParkingFinder.base import Session

session = Session()


@contextmanager
def create_session():
    """Provide a transactional scope around a series of operations."""
    try:
        yield session
        session.commit()
    except Return:
        session.commit()
        raise
    except:
        session.rollback()
        raise


def close_session():
    session.close()


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
            yield method(session=_session, *args, **params)
            session.commit()
        except Return:
            session.commit()
            raise
        except:
            session.rollback()
            raise

    return wrapper
