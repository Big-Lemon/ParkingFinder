from sqlalchemy.orm.exc import NoResultFound
from tornado.gen import coroutine, Return

from ParkingFinder.base.async_db import create_session
from ParkingFinder.base.errors import NotFound
from ParkingFinder.mappers.user_mapper import UserMapper
from ParkingFinder.tables.user import Users


class UserRepository(object):

    @staticmethod
    @coroutine
    def read_one(user_id):
        """
        Read one user by user_id

        :param str user_id:
        :return User:
        :raises sqlalchemy.orm.exc.NoResultFound:
        """
        with create_session() as session:
            user = session.query(Users).filter(
                Users.user_id == user_id
            ).one()
            entity = UserMapper.to_entity(record=user)
            raise Return(entity)

    @classmethod
    @coroutine
    def upsert(cls, user):
        """
        Update/Insert user, if user exist, update user's information
        otherwise, insert a new user, and user have to be a user entity
        with all required fields

        :param User user:
        :return User:
        :raises AssertionError: the user provided doesn't have user_id
        :raises ValidationError: the user provided missing required fields
        """
        assert user.user_id

        try:
            _user = yield cls._update(
                user_id=user.user_id,
                activated_vehicle=user.activated_vehicle,
                profile_picture_url=user.profile_picture_url
            )
            raise Return(_user)

        except NoResultFound:
            _user = yield cls._insert(user)
            raise Return(_user)

    @classmethod
    @coroutine
    def _update(cls,
                user_id,
                activated_vehicle=None,
                profile_picture_url=None,
                ):
        """

        :param str user_id:
        :param str activated_vehicle:
        :param str profile_picture_url:
        :return User: updated User
        :raises NoResultFound: the user that is requested to update is not exist
        """

        with create_session() as session:
            user = session.query(Users).filter(
                Users.user_id == user_id
            ).one()

            if activated_vehicle:
                user.activated_vehicle = activated_vehicle

            if profile_picture_url:
                user.profile_picture_url = profile_picture_url

            entity = UserMapper.to_entity(user)

            raise Return(entity)

    @staticmethod
    @coroutine
    def _insert(user):
        """
        Insert a new user into db

        :param User user: complete entity will all required fields
        :return User: Inserted User
        """
        with create_session() as session:
            user.validate()
            _user = UserMapper.to_model(user)
            session.add(_user)
            raise Return(user)


class UserNotFound(NotFound):
    error = 'User Not Found'
