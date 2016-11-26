import httplib
import json

from tornado.gen import coroutine

from ParkingFinder.base.errors import (
    NotFound,
    with_exception_handler
)
from ParkingFinder.base.validate_access_token import with_token_validation
from ParkingFinder.entities.vehicle import Vehicle
from ParkingFinder.handlers.handler import BaseHandler
from ParkingFinder.mappers.user_mapper import UserMapper
from ParkingFinder.repositories.access_token_repository import AccessTokenRepository
from ParkingFinder.services.user import UserService


class UserInformationHandler(BaseHandler):

    @with_exception_handler
    @with_token_validation
    @coroutine
    def get(self, user_id):
        """
        handle the get request from /user/{user_id}?access_token={access_token}
        and write it back with proper fetched user information

        :param String user_id:
        :return:
        """
        assert user_id
        user = yield UserService.get_user_detail(
            user_id=user_id
        )
        result_string = UserMapper.to_record(user)

        self.set_status(httplib.OK)
        self.write(result_string)

    @with_exception_handler
    @with_token_validation
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
        assert user_id
        user = yield UserService.get_user_detail(
            user_id=user_id
        )

        # json.loads() for string or unicode
        # json load() for file
        request_body = json.loads(self.request.body)
        activated_vehicle_plate = request_body.get('activated_vehicle')
        new_vehicle = request_body.get('new_vehicle', False)
        if new_vehicle:
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
            self.set_status(httplib.OK)

        if activated_vehicle_plate:
            # active_vehicle will throw NotFound if the user
            # doesn't own the vehicle with given plate
            yield UserService.activate_vehicle(
                user_id=user.user_id,
                vehicle_plate=activated_vehicle_plate
            )
            self.set_status(httplib.OK)

    @with_exception_handler
    @with_token_validation
    @coroutine
    def put(self, user_id):
        """
        logout
        :param user_id:
        :return:
        """
        payload = json.loads(self.request.body or '{}')
        access_token = payload.get("access_token", None)
        assert access_token and user_id
        yield AccessTokenRepository.remove(access_token=access_token)
        self.write(httplib.OK)
