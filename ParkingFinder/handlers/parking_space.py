import httplib
import json

from datetime import datetime
from tornado.gen import coroutine
from tornado.web import MissingArgumentError

from ParkingFinder.handlers.handler import BaseHandler
from ParkingFinder.mappers.parking_space_mapper import ParkingSpaceMapper
from ParkingFinder.services.user import UserService
from ParkingFinder.entities.parking_space import ParkingSpace
from ParkingFinder.base.errors import (
    NotFound,
)


class ParkingSpaceNearbyFetchHandler(BaseHandler):

    @coroutine
    def get(self, user_id):

        try:
            access_token = self.get_argument('access_token', default=None)
            # TODO: token validation
            assert user_id
            location_x = self.get_argument('x')
            location_y = self.get_argument('y')
            radius = self.get_argument('radius')

            parking_space_list = []
            # TODO: get the list of free parking space in checkout table entity from service layer

            # current temp space list

            parking_space_list.append(ParkingSpace({
                'user_id': 'laodiji',
                'latitude': 137.81,
                'longitude': 127.10,
                'created_at': datetime.utcnow(),
            }))

            parking_space_list.append(ParkingSpace({
                'user_id': 'feishfu',
                'latitude': 99.81,
                'longitude': 00.10,
                'created_at': datetime.utcnow(),
            }))
            ########################################
            space_list = [ParkingSpaceMapper.to_record(space) for space in parking_space_list]

            self.set_status(httplib.OK)
            self.write({
                'spaces': space_list
            })

        except AssertionError:
            self.set_status(httplib.BAD_REQUEST)
            self.write({
                'error': "BAD REQUEST Invalid User Id"
            })
        except MissingArgumentError:
            self.set_status(httplib.BAD_REQUEST)
            self.write({
                'error': "BAD REQUEST Location Information Is Incomplete"
            })
        except NotFound:
            self.set_status(httplib.NOT_FOUND)
            self.write({
                'error': "user doesn't exist according to current provided id"
            })


class ParkingSpaceReserveHandler(BaseHandler):

    @coroutine
    def post(self, user_id):

        try:
            access_token = self.get_argument('access_token', default=None)
            # TODO: token validation
            assert user_id
            user = yield UserService.get_user_detail(
                user_id=user_id
            )
            request_body = json.loads(self.request.body)
            coordinate = request_body.get('coordinate', False)
            location_x = coordinate['x']
            location_y = coordinate['y']
            # TODO: put the location x and y into reserve table

            parking_space_list = []
            # current temp space list
            parking_space_list.append(ParkingSpace({
                'user_id': 'laodiji',
                'latitude': 137.81,
                'longitude': 127.10,
                'created_at': datetime.utcnow(),
            }))

            parking_space_list.append(ParkingSpace({
                'user_id': 'feishfu',
                'latitude': 99.81,
                'longitude': 00.10,
                'created_at': datetime.utcnow(),
            }))
            ########################################
            spaceList = [ParkingSpaceMapper.to_record(space) for space in parking_space_list]

            self.set_status(httplib.OK)
            self.write({
                'spaces': spaceList
            })
        except AssertionError:
            self.set_status(httplib.BAD_REQUEST)
            self.write({
                'error': "BAD REQUEST Invalid User Id"
            })
        except NotFound:
            self.set_status(httplib.NOT_FOUND)
            self.write({
                'error': "user doesn't exist according to current provided id"
            })


