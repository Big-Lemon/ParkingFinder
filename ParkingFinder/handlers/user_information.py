import httplib

from tornado.gen import coroutine

from ParkingFinder.base.errors import (
    NotFound,
)
from ParkingFinder.services.user import UserService
from ParkingFinder.mappers.user_mapper import UserMapper
from ParkingFinder.handlers.handler import BaseHandler




class UserInformationHandler(BaseHandler):

    @coroutine
    def get(self, user_id):

        access_token = self.get_argument('access_token')
        # to do : token validation

        try:
            assert user_id
            user = yield UserService.get_user_detail(
                user_id=user_id
            )
            result_string = UserMapper.to_record(user)

            self.set_status(httplib.OK)
            self.write(result_string)

        except NotFound:
            self.set_status(httplib.NOT_FOUND)
            self.write({
                'error': "user doesn't exist according to current provided id"
            })
        except AssertionError:
            self.set_status(httplib.BAD_REQUEST)
            self.write({
                'error': "BAD REQUEST Invalid User Id"
            })




