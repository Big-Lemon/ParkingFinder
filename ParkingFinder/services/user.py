# -*- coding: utf-8 -*-
"""User Service.

This module contains all the service method related to user's information, which
includes access_token, update/remove/modify user's information. update the vehicles
owned by users

Flow:
    1. Inspect access token
    2. Check existence of user
    3. Register user if not exist
    4. Register new vehicle
    5. Activate Vehicles

Todo:
    * Move logic of inspecting access token from handler to UserService


"""

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


class UserService(object):

    @classmethod
    @coroutine
    def update_access_token(cls, access_token):
        """
        Update the expiration time of access token if it is already exist,
        otherwise, create a new access_token. If the the owner of the access token
        already has an account, return the user entity, otherwise throw UserNotFound
        Exception to indicate the caller the user is first time login.

        :param AccessToken access_token:
        :return AccessToken:
        :raises UserNotFound:
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
        Update user's activated vehicle if exist
        create a new user otherwise.

        TODO:
            * Handler could directly call repository's upsert method since this is atom operation

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
        Link a new vehicle to the user.

        :param String user_id: user's user id
        :param Vehicle vehicle: vehicle object that contains all the information
        :raise: NotFound: User doesn't exist in database
        :raise: InvalidEntity: Vehicle entity contains invalid fields or missing fields
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

        :param String user_id: user's id
        :raise: NotFound : user doesn't exist
        :return: User user: user entity contains detailed information and linked vehicles
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

        :param String user_id: user's id
        :param String vehicle_plate: the plate of vehicle to be activated
        :raise: NotFound: user doesn't exist
        :return: User user: updated user entity
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



