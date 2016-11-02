from sqlalchemy.orm.exc import NoResultFound
from schematics.exceptions import ValidationError
from tornado.gen import coroutine, Return

from ParkingFinder.base.errors import (
    NotFound,
    InvalidEntity,
)
from ParkingFinder.repositories.access_token_repository import AccessTokenRepository
from ParkingFinder.repositories.user_repository import (
    UserNotFound,
    UserRepository,
)
from ParkingFinder.repositories.vehicle_repository import VehicleRepository
from clay import config

logger = config.get_logger('user')


# the correct flow is to 1.register user first then 2.register a car and finally 3.activate a car
# to avoid code redundancy, there will be no condition implemented such that each step calls its previous step inside
class UserService(object):

    @classmethod
    @coroutine
    def update_access_token(cls, access_token):
        """
        update/create expiration date of access_token, and create
        user if not exist, otherwise, return user's information

        :param AccessToken access_token:
        :return AccessToken:
        """
        access_token.validate()
        token = yield AccessTokenRepository.upsert(
            access_token=access_token.access_token,
            expires_at=access_token.expires_at,
            user_id=access_token.user_id,
            issued_at=access_token.issued_at,
        )
        try:
            access_token = yield AccessTokenRepository.read_one(
                access_token=token.access_token
            )
            raise Return(access_token)

        except UserNotFound:
            logger.info('New user login: ' + token.user_id)
            raise NotFound

    @staticmethod
    @coroutine
    def register(user):
        """
        Register a new user if not exist and register a vehicle for the user
        this have checked if the car exist or not

        :param: User user:
        :raise: InvalidEntity: means the constructed entity is not consistent with its definition
        :return: User Updated User
        """
        try:
            user.validate()
        except ValidationError:
            raise InvalidEntity

        _user = yield UserRepository.upsert(user=user)

        raise Return(_user)

    @staticmethod
    @coroutine
    def register_vehicle(user_id, vehicle):
        """
        register a vehicle for the user and this have checked if the car exist or not

        :param String user_id:
        :param Vehicle vehicle:
        :raise: NotFound: requested value is not found in the database
        :raise: InvalidEntity
        :return: Vehicle vehicle: inserted vehicle
        """

        try:
            vehicle.validate()
            user = yield UserRepository.read_one(user_id)
            user_vehicles = yield VehicleRepository.retrieve_vehicle_by_user(user_id=user.user_id)
            exist = False
            for current_vehicle in user_vehicles:
                if current_vehicle.plate == vehicle.plate:
                    _vehicle = current_vehicle
                    exist = True
                    break
            if not exist:
                _vehicle = VehicleRepository.insert_registered_vehicle(user_id=user.user_id, vehicle=vehicle)
        except NoResultFound:
            raise NotFound
        except ValidationError:
            raise InvalidEntity

        raise Return(_vehicle)


    @staticmethod
    @coroutine
    def get_user_detail(user_id):
        """
        Return the user information in detail with registered car information

        :param String user_id:
        :raise: NotFound : user detail cannot be found
        :return: User user:
        """
        try:
            user = yield UserRepository.read_one(user_id=user_id)
            user_vehicles = yield VehicleRepository.retrieve_vehicle_by_user(user_id=user_id)
            user.owned_vehicles = user_vehicles
        except NoResultFound:
            raise NotFound

        raise Return(user)

    @staticmethod
    @coroutine
    def activate_vehicle(user_id, vehicle_plate):
        """
        activate an vehicle of a user
        if user want to activate a car that he doesn't own then he won't be allowed to do so
        In order to avoid redundancy, This implementation will not help user to register car here
        So He must register first in order to activate it so the return value can be
        an indicator since if its activated vehicle has been changed => activate successfully
        otherwise activation failure means call register function first

        :param String user_id:
        :param String vehicle_plate:
        :raise: NotFound: user detail cannot be found
        :return: updated user:
        """
        try:
            user = yield UserRepository.read_one(user_id)
            user_vehicles = yield VehicleRepository.retrieve_vehicle_by_user(user_id=user.user_id)
            exist = False
            for current_vehicle in user_vehicles:
                if current_vehicle.plate == vehicle_plate:
                    exist = True
                    break
            if exist and (user.activated_vehicle != vehicle_plate):
                user.activated_vehicle = vehicle_plate
                _user = yield UserRepository.upsert(user=user)
            else:
                _user = user
        except NoResultFound:
            raise NotFound

        raise Return(_user)



