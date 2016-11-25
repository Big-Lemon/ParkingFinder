import httplib
import json

from tornado.gen import coroutine, Return

from ParkingFinder.base.errors import InvalidArguments, NotFound, with_exception_handler
from ParkingFinder.base.validate_access_token import with_token_validation
from ParkingFinder.base.errors import Timeout
from ParkingFinder.entities.parking_space import ParkingSpace
from ParkingFinder.entities.waiting_user import WaitingUser
from ParkingFinder.handlers.handler import BaseHandler
from ParkingFinder.mappers.available_parking_space_mapper import AvailableParkingSpaceMapper
from ParkingFinder.mappers.parking_space_mapper import ParkingSpaceMapper
from ParkingFinder.mappers.vehicle_mapper import VehicleMapper
from ParkingFinder.repositories.googleAPI import TranslateAddressService
from ParkingFinder.repositories.parking_lot import ParkingLotRepository
from ParkingFinder.repositories.vehicle_repository import VehicleRepository
from ParkingFinder.repositories.available_parking_space_pool import AvailableParkingSpacePool
from ParkingFinder.services.user import UserService
from ParkingFinder.services.parking_space import ParkingSpaceService
from ParkingFinder.services.user_request import UserRequestService, CanNotStopForwardingMessage


class RequestParkingSpaceHandler(BaseHandler):
    """
    Handle Request Parking Space
nn
    """
    @with_exception_handler
    @with_token_validation
    @coroutine
    def put(self, user_id):
        """

        request format: {
            "longitude": 123.123,
            "latitude": 123.456,
            "level": None,
            "address": None,
        }

        return format: {
            "available_parking_spaces": [
            {
                'plate': '1234567',
                'latitude': 123.123,
                'longitude': 123.456,
                'address': None,
                'level': None
            }
            ]
        }

        BAD_REQUEST: the user passed in is not valid or user terminates
            the service during transition
        REQUEST_TIMEOUT: the request timeout, cliend could send request again

        :param user_id:
        :return:
        """
        assert user_id
        payload = json.loads(self.request.body)
        longitude = payload.get("longitude", None)
        latitude = payload.get("latitude", None)
        assert longitude and latitude

        user = yield UserService.get_user_detail(user_id=user_id)
        assert user.activated_vehicle

        waiting_user = WaitingUser({
            'user_id': user_id,
            'location': {
                'longitude': longitude,
                'latitude': latitude
            },
        })

        available_parking_spaces = yield UserRequestService.request_parking_space(
            waiting_user=waiting_user
        )

        _spaces = [
            AvailableParkingSpaceMapper.to_record(entity=parking_space)
            for parking_space in available_parking_spaces
            ]

        self.set_status(httplib.OK)
        self.write({
            'available_parking_spaces': _spaces
        })




class PostParkingSpaceHandler(BaseHandler):
    """
    Handle Post parking space request
    """

    @with_exception_handler
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
            "parking_space": {
                "plate" : "1234567",
                "latitude": 123.123,
                "longitude": 123.144,
                # optional
                "level": None,
                "address": "parking lot 7"
            }
        }

        REQUEST_TIMEOUT: request timeout, client could send the request again to keep
            in the matching queue

        :param String user_id:
        :return:
        """
        assert user_id
        payload = json.loads(self.request.body)
        plate = payload.get("plate", False)
        assert plate

        if (yield _verify_vehicle_belonging(user_id=user_id, plate=plate)):
            parking_space = yield ParkingSpaceService.post_parking_space(plate=plate)
            _response = ParkingSpaceMapper.to_record(entity=parking_space)
            self.set_status(httplib.OK)
            self.write({
                "parking_space": _response
            })

        else:
            raise InvalidArguments


class ReserveParkingSpaceHandler(BaseHandler):
    """
    Reserve Parking Space
    """

    @with_exception_handler
    @with_token_validation
    @coroutine
    def post(self, user_id):
        """
            Reserve a parking space
            request format:
            {
                "plate": "1234567"
            }
            token is parking car plate
            response format:
            {
                "parking_space": {
                    "plate": "1234567"
                    "latitude": "123.123",
                    "longitude": "123.123",

                    # optional
                    "level": None,
                    "address": 'ucla parking lot 7'

                },
                "vehicle": {
                    "plate": "1234567",
                    "model": "civic",
                    "brand": "honda",
                    "color": "white",
                    "year": "year",
                    "vehicle_picture": None

                }

            }

            :param String user_id:
            :return:
        """
        assert user_id
        payload = json.loads(self.request.body)
        plate = payload.get("plate", False)
        assert plate

        parking_space = yield UserRequestService.accept_parking_space(user_id=user_id, accepted_space_plate=plate)

        vehicle = yield VehicleRepository.retrieve_vehicle_by_plate(plate=parking_space.plate)

        _parking_space = ParkingSpaceMapper.to_record(entity=parking_space)
        _vehicle = VehicleMapper.to_record(entity=vehicle)

        self.set_status(httplib.OK)
        self.write({
            'vehicle': _vehicle,
            'parking_space': _parking_space
        })

class RejectParkingSpaceHandler(BaseHandler):

    @with_exception_handler
    @with_token_validation
    @coroutine
    def post(self, user_id):
        """
        Reject all parking spaces
        request format: {}
        return format:
        {
            # available pakring spaces could be a empty list if no availlable parking spaces
            "available_parking_spaces": [
                {
                    'plate': '1234566',
                    'longitude': 123.123,
                    'latitude': 123.456,
                    'address': 'ucla parking lot 7',
                    'level': 7
                },
                {
                    'plate': '1234567',
                    'longitude': 124.123,
                    'latitude': 125.456,
                    'address': None,
                    'level': None
                }
            ]
        }

        :param user_id:
        :return:
        """
        assert user_id
        available_parking_spaces = yield UserRequestService.reject_all_parking(user_id=user_id)
        self.set_status(httplib.OK)

        if available_parking_spaces:
            _available_parking_spaces = [AvailableParkingSpaceMapper.to_record(
                entity=available_parking_space
            ) for available_parking_space in available_parking_spaces]
            self.write({
                    'available_parking_spaces': _available_parking_spaces
                })
        else:
            self.write({
                'available_parking_spaces': []
            })


class ParkingLotHandler(BaseHandler):

    @with_exception_handler
    @with_token_validation
    @coroutine
    def post(self, user_id):
        """
        Check out

        :param user_id:
        :return:
        """
        assert user_id
        payload = json.loads(self.request.body)
        plate = payload.get("plate", False)

        assert plate

        is_valid_plate = yield _verify_vehicle_belonging(user_id=user_id, plate=plate)
        if is_valid_plate:
            # TODO if the user checkout before connection established with a waiting user.
            removed = yield ParkingLotRepository.remove(plate=plate)
            if not removed:
                raise InvalidArguments
            self.set_status(httplib.OK)

        else:
            raise InvalidArguments

    @with_exception_handler
    @with_token_validation
    @coroutine
    def put(self, user_id):
        """
        Check in
        request format:
        {
            "plate": "123456",
            "longitude": 123.123,
            "latitude": 456.123,
            "level": None
        }

        return format:
        {
            "parking_space": {
                "plate": "123456",
                "longitude": 123.123,
                "latitude": 456.123,
                "level": None,
                "address": "ucla parking lot 7"
            }
        }
        :param user_id:
        :return:
        """
        assert user_id
        payload = json.loads(self.request.body)
        plate = payload.get("plate", None)
        longitude = payload.get("longitude", None)
        latitude = payload.get("latitude", None)
        # TODO convert longitude & latitude to address before insert into parking lot
        assert plate and longitude and latitude
        address = yield TranslateAddressService.getAddressBylatlng(latitude,longitude)
        is_valid_plate = yield _verify_vehicle_belonging(user_id=user_id, plate=plate)
        if is_valid_plate:
            parking_space = yield ParkingLotRepository.insert(
                parking_space=ParkingSpace({
                    'plate': plate,
                    'location': {
                        'longitude': longitude,
                        'latitude': latitude,
                        'location': str(address)
                    }
                }))
            # remove user from user waiting pool has been handled in the
            # user_request so do not handle this here
            # yield UserRequestService.service_terminate(user_id=user_id)
            _parking_space = ParkingSpaceMapper.to_record(entity=parking_space)
            self.set_status(httplib.OK)
            self.write({
                'parking_space': _parking_space
            })
        else:
            raise InvalidArguments

    @with_exception_handler
    @with_token_validation
    @coroutine
    def get(self, user_id):
        """
        fetch nearby
        input format
        {
            "longitude": -117.844379,
            "latitude": 34.044742,
        }
        the parking space around it
        return format:
        {"available_parking_spaces": [
            {
            "latitude": 34.044742, 
            "plate": "6DAY434", 
            "longitude": -117.84431, 
            "expired_at": "2017-11-24 23:36:26.222000"
            }, 
            {
            "latitude": 34.044729, 
            "plate": "6ELA725", 
            "longitude": -117.844213, 
            "expired_at": "2017-11-24 23:36:26.123000"
            }
            ]
        }
        """
        assert user_id
        longitude = self.get_argument("longitude", False)
        latitude = self.get_argument("latitude", False)
        assert longitude and latitude
        print longitude
        print latitude
        nearby_available_parking_spaces = yield AvailableParkingSpacePool.read_many(longitude=longitude,latitude=latitude)
        print nearby_available_parking_spaces
        self.set_status(httplib.OK)
        _available_parking_spaces = [AvailableParkingSpaceMapper.to_record(
                entity=single_available_parking_space
            ) for single_available_parking_space in nearby_available_parking_spaces]
        self.write({
                'available_parking_spaces': _available_parking_spaces
            })


class ServiceTerminateHanlder(BaseHandler):

    @with_exception_handler
    @with_token_validation
    @coroutine
    def post(self, user_id):
        """
        terminate the service in the requester side
        :param user_id:
        :return:
        """
        assert user_id
        try:
            yield UserRequestService.service_terminate(user_id=user_id)
            self.set_status(httplib.OK)
        except CanNotStopForwardingMessage:
            self.set_status(httplib.BAD_REQUEST)
            self.write({
                'massage': 'too late to stop the service'
            })


@coroutine
def _verify_vehicle_belonging(user_id, plate):

    user = yield UserService.get_user_detail(user_id=user_id)
    if not user.owned_vehicles:
        raise Return(False)

    if not (user.activated_vehicle == plate or any([
            plate == vehicle.plate for vehicle in user.owned_vehicles
            ])):
        raise Return(False)

    else:
        raise Return(True)
