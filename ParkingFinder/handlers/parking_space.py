import httplib
import json

from datetime import datetime
from tornado.gen import coroutine, Return

from ParkingFinder.base.errors import InvalidArguments, NotFound
from ParkingFinder.base.validate_access_token import with_token_validation
from ParkingFinder.base.with_repeat import Timeout
from ParkingFinder.handlers.handler import BaseHandler
from ParkingFinder.mappers.real_time_location_mapper import RealTimeLocationMapper
from ParkingFinder.mappers.available_parking_space import AvailableParkingSpaceMapper
from ParkingFinder.mappers.parking_space_mapper import ParkingSpaceMapper
from ParkingFinder.repositories.parking_lot import ParkingLotRepository
from ParkingFinder.services.user import UserService
from ParkingFinder.services.parking_space import ParkingSpaceService
from ParkingFinder.services.real_time_location_service import RealTimeLocationService
from ParkingFinder.services.user_request import UserRequestService

#每次返回的时候要加上2个list 的 车的
class PostParkingSpaceHandler(BaseHandler):

    @with_token_validation
    @coroutine
    def put(self, user_id):
        """
        Put request to post a parking space
        request format:
        {
            "plate": "1234567"
        }
        token is parking car plate
        response format:
        {
            "token": "1234567",
            "latitude": "123.123",
            "longitude": "123.123",

            # optional
            "level": 1,
            "description": 'ucla parking lot 7'
            "vehicle_picture": 

            #Noimplemented
            "plate":
            "model":
            "brand":
            "color":
        }

        :param String user_id:
        :return:
        """

        try:
            payload = json.loads(self.request.body)
            plate = payload.get("plate", False)

            assert plate

            if (yield _verify_vehicle_belonging(user_id=user_id, plate=plate)):
                parking_space = yield ParkingSpaceService.post_parking_space(plate=plate)
                #need to add car information
                _response = ParkingSpaceMapper.to_record(entity=parking_space)
                self.set_status(httplib.OK)
                self.write(_response)

            else:
                raise InvalidArguments

        except Timeout:
            self.set_status(httplib.OK)
            self.write({})

        except NotFound:
            self.set_status(httplib.BAD_REQUEST)
            self.write({
                'error': 'The Vehicle With Given Plate Have Not Been Checked In Yet'
            })

        except (AssertionError, InvalidArguments):
            self.set_status(httplib.BAD_REQUEST)
            self.write({
                'error': 'Bad Request'
            })


class ReserveParkingSpaceHandler(BaseHandler):

    @with_token_validation
    @coroutine
    def post(self, user_id):
    """
        Reserve a parking space
        request format:
        {
            "user_id": "account_1"
            "accepted_space_plate": "1234567"
        }
        token is parking car plate
        response format:
        {
            "token": "1234567",
            "latitude": "123.123",
            "longitude": "123.123",

            # optional
            "level": 1,
            "description": 'ucla parking lot 7'
            "vehicle_picture": 

            #Noimplemented
            "plate":
            "model":
            "brand":
            "color":
        }

        :param String user_id:
        :return:
    """
        try:
            payload = json.loads(self.request.body)
            plate = payload.get("plate", False)
            assert plate

            parking_space = yield UserRequestService.accept_parking_space(user_id=user_id, accepted_space_plate=plate)

            #need to add car information

            response = ParkingSpaceMapper.to_record(entity=parking_space)
            self.set_status(httplib.OK)
            self.write(response)

            if not plate:
                yield UserRequestService.reject_all_parking(user_id=user_id)
                self.set_status(httplib.OK)
            else:
                pass

        except Timeout:
            self.set_status(httplib.OK)
            self.write({
                'error': 'Reservation Expired'
            })

        except AssertionError:
            self.set_status(httplib.BAD_REQUEST)
            self.write({
                'error': 'Missing Plate'
            })


class RejectParkingSpaceHandler(BaseHandler):

    @with_token_validation
    @coroutine
    def post(self, user_id):
        try:
            available_parking_spaces = yield UserRequestService.reject_all_parking(user_id=user_id)
            self.set_status(httplib.OK)
            if available_parking_spaces:
                _response = AvailableParkingSpaceMapper.to_record(entity=available_parking_spaces)
                self.write(_response)
            else:
                self.write(None)

        except Timeout:
            self.set_status(httplib.OK)
            self.write({
                'error': 'Reservation Expired'
            })


class ParkingLotHandler(BaseHandler):

    @with_token_validation
    @coroutine
    def post(self, user_id):
        """
        Check out

        :param user_id:
        :return:
        """
        try:
            payload = json.loads(self.request.body)
            plate = payload.get("plate", False)

            assert plate

            if (yield _verify_vehicle_belonging(user_id=user_id, plate=plate)):
                removed = yield ParkingLotRepository.remove(plate=plate)
                yield RealTimeLocationService.terminate_real_time_location(token=plate)
                if not removed:
                    raise InvalidArguments
                self.set_status(httplib.OK)

            else:
                raise InvalidArguments

        except InvalidArguments:
            self.set_status(httplib.BAD_REQUEST)

    @with_token_validation
    @coroutine
    def put(self, user_id):
        """
        Check in
        :param user_id:
        :return:
        """
        try:
            payload = json.loads(self.request.body)
            plate = payload.get("plate", None)
            token = payload.get("token", None)

            assert plate

            if (yield _verify_vehicle_belonging(user_id=user_id, plate=plate)):
                removed = yield ParkingLotRepository.remove(plate=plate)
                yield UserRequestService.service_terminate(user_id=user_id)
                yield RealTimeLocationService.terminate_real_time_location(token=token, user_id=user_id)
                if not removed:
                    raise InvalidArguments
                self.set_status(httplib.OK)
            else:
                raise InvalidArguments
        except InvalidArguments:
            self.set_status(httplib.BAD_REQUEST)


def _verify_vehicle_belonging(user_id, plate):

    user = yield UserService.get_user_detail(user_id=user_id)
    if not user.owned_vehicle:
        raise Return(False)

    if not user.owned_vehicle:
        raise Return(False)
    if not (user.activated_vehicle == plate or any([
            plate == vehicle.plate for vehicle in user.owned_vehicle
            ])):
        raise Return(False)

    else:
        raise Return(True)
