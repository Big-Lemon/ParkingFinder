from contextlib import contextmanager
from tornado.gen import Return

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
