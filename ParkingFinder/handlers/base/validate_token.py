import functools
import httplib

from sqlalchemy.orm.exc import NoResultFound
from tornado.gen import coroutine, Return

from ParkingFinder.repositories.access_token_repository import AccessTokenRepository
from ParkingFinder.base.errors import InvalidArguments


def validate_token(method):
    """Decorate methods with this to require that the user be logged in.

    If the user is not logged in, they will be redirected to the configured
    `login url <RequestHandler.get_login_url>`.

    If you configure a login url with a query parameter, Tornado will
    assume you know what you're doing and use it as-is.  If not, it
    will add a `next` parameter so the login page knows where to send
    you once you're logged in.
    """
    @functools.wraps(method)
    @coroutine
    def wrapper(self, *args, **kwargs):
        input_token = self.get_argument('access_token', None)
        try:
            assert input_token
            token = yield AccessTokenRepository.read_one(access_token=input_token)
            if token.is_expired:
                raise InvalidArguments
        except NoResultFound:
            self.set_status(httplib.UNAUTHORIZED)
            self.write({
                'error': 'Invalid Access Token',
                'payload': {
                    'access_token': input_token
                }
            })
            raise Return()
        except InvalidArguments:
            self.set_status(httplib.BAD_REQUEST)
            self.write({
                'error': 'Access Token Expired',
                'payload': {
                    'access_token': input_token,
                }
            })
        except AssertionError:
            self.set_status(httplib.BAD_REQUEST)
            self.write({
                'error': 'Missing Access Token',
            })
            raise Return()
        raise Return(method(self, *args, **kwargs))
    return wrapper
