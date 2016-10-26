from sqlalchemy.orm.exc import NoResultFound
from tornado.gen import coroutine, Return

from ParkingFinder.base.errors import (
    NotFound,
)
from ParkingFinder.repositories.access_token_repository import AccessTokenRepository
from ParkingFinder.repositories.user_repository import (
    UserNotFound,
    UserRepository,
)


class UserService(object):

    @classmethod
    @coroutine
    def login(cls, access_token):
        """
        update/create expiration date of access_token, and create
        user if not exist, otherwise, return user's information

        :param AccessToken access_token:
        :return:
        """
        access_token.validate()
        token = yield AccessTokenRepository.upsert(
            access_token=access_token.access_token,
            expires_at=access_token.expires_at,
            user_id=access_token.user_id,
            issued_at=access_token.issued_at,
        )
        try:
            user = yield cls.get_user_detail(
                user_id=token.user_id
            )
            raise Return(user)

        except UserNotFound:
            raise NotFound

    @staticmethod
    @coroutine
    def register(user, vehicle=None):
        """
        Register a new user if not exist

        :param User user:
        :param Vehicle vehicle:
        :return:
        """
        user.validate()
        if vehicle:
            vehicle.validate()

        _user = yield UserRepository.upsert(user=user)

        raise Return(_user)

        # TODO if vehicle not None, add to vehicle repository

    @staticmethod
    @coroutine
    def logout(access_token):
        """
        Log out a user by access_token

        :param str access_token:
        :return:
        """
        try:
            yield AccessTokenRepository.remove(
                access_token=access_token
            )
        except NoResultFound:
            raise NotFound

        raise Return()

    @staticmethod
    @coroutine
    def get_user_detail(user_id):
        try:
            user = yield UserRepository.read_one(user_id=user_id)
            # TODO read vehicles from vehicle repository and assign to user entity
        except NoResultFound:
            raise NotFound

        raise Return(user)
