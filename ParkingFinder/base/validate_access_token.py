import functools
import httplib
import json
from sqlalchemy.orm.exc import NoResultFound
from tornado.gen import coroutine

from ParkingFinder.base.errors import Unauthorized
from ParkingFinder.repositories.access_token_repository import AccessTokenRepository


def with_token_validation(f):

    @coroutine
    @functools.wraps(f)
    def wrapper(self, user_id, *args, **params):
        payload = json.loads(self.request.body)
        access_token = self.get_argument('access_token', payload.get("access_token", False))
        try:
            if not access_token:
                raise Unauthorized

            try:
                token = yield AccessTokenRepository.read_one(
                    access_token=access_token
                )
                if token.user_id != user_id:
                    raise Unauthorized

            except NoResultFound:
                raise Unauthorized
            yield f(self, user_id=user_id, *args, **params)
        except Unauthorized:
            self.set_status(httplib.UNAUTHORIZED)
            self.write({
                "error": "Invalid Access Token",
                "payload": {
                    "access_token": access_token
                }
            })

    return wrapper
