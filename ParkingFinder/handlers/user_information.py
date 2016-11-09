import httplib
import json

from tornado.gen import coroutine

from ParkingFinder.base.errors import (
    NotFound,
    InvalidEntity,
)
from ParkingFinder.base.validate_access_token import with_token_validation
from ParkingFinder.entities.user import User
from ParkingFinder.entities.vehicle import Vehicle
from ParkingFinder.handlers.handler import BaseHandler
from ParkingFinder.mappers.user_mapper import UserMapper
from ParkingFinder.services.user import UserService


class UserInformationHandler(BaseHandler):

    @with_token_validation
    @coroutine
    def get(self, user_id):
        """
        handle the get request from /user/{user_id}?access_token={access_token}
        and write it back with proper fetched user information

        :param String user_id:
        :return:
        """
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

    @coroutine
    def post(self, user_id):
        """
        handle the post request from /user/{user_id}?access_token={access_token}
        and use the information in the request body to update the database properly
        simple code to send post request and body json format
        curl -i -d
        '{
            "activated_vehicle":"laosiji",
            "new_vehicle" :{
                "plate":"laosiji",
                "brand":"toyoto",
                "model":"hongqi",
                "color":"blue",
                "year":"1950"
                }
        }'
        http://localhost:8888/user/{user_id}?access_token={access_token}

        :param String user_id:
        :return:
        """
        # set to default to avoid missingArgumentException
        access_token = self.get_argument(name='access_token', default=None)
        # TODO: token validation
        try:
            assert user_id
            user = yield UserService.get_user_detail(
                user_id=user_id
            )

            # json.loads() for string or unicode
            # json load() for file
            request_body = json.loads(self.request.body)
            activated_vehicle_plate = request_body.get('activated_vehicle')
            new_vehicle = request_body.get('new_vehicle', False)
            flow_check = True
            if new_vehicle:
                try:
                    vehicle = Vehicle({
                        'plate': new_vehicle['plate'],
                        'brand': new_vehicle['brand'],
                        'model': new_vehicle['model'],
                        'color': new_vehicle['color'],
                        'year': new_vehicle['year']
                    })
                    # since NotFound has been handled in get_user_detail() so no need to try here
                    # but we have to handle the invalid entity exception
                    yield UserService.register_vehicle(user.user_id, vehicle)
                except InvalidEntity:
                    flow_check = False
                    self.set_status(httplib.BAD_REQUEST)
                    self.write({
                        'error': "BAD REQUEST new vehicle info is incomplete \n"
                    })

            if activated_vehicle_plate and flow_check:
                # since NotFound has been handled in get_user_detail() so no need to try here
                user = yield UserService.activate_vehicle(user.user_id, activated_vehicle_plate)
                if user and user.activated_vehicle != activated_vehicle_plate:
                    flow_check = False
                    self.set_status(httplib.BAD_REQUEST)
                    self.write({
                        'error': "BAD REQUEST please register the vehicle with user first \n"
                    })

            if (not activated_vehicle_plate) and (not new_vehicle):
                self.set_status(httplib.BAD_REQUEST)
                self.write({
                    'error': "BAD REQUEST new vehicle info and activated vehicle info are both invalid \n"
                })
            elif flow_check:
                self.set_status(httplib.OK)
                self.write("you have update the info successfully \n")

        except NotFound:
            self.set_status(httplib.NOT_FOUND)
            self.write({
                'error': "user doesn't exist according to current provided id, please correct or register first \n"
            })
        except AssertionError:
            self.set_status(httplib.BAD_REQUEST)
            self.write({
                'error': "BAD REQUEST Invalid User Id \n"
            })


