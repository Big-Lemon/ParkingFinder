from sqlalchemy.orm.exc import NoResultFound
from tornado.gen import coroutine, Return

from ParkingFinder.base.async_db import create_session
from ParkingFinder.base.errors import NotFound
from ParkingFinder.mappers.parking_space_mapper import CheckOutParkingSpaceMapper
from ParkingFinder.tables.check_out_parking_space import CheckOutParkingSpace


class CheckOutParkingSpaceRepository(object):

    @staticmethod
    @coroutine
    def read_one(user_id):
        """

        :param str user_id:
        :return ParkingSpace parking_space:
        """
        with create_session() as session:
            parking_space = session.query(CheckOutParkingSpace).filter(
                CheckOutParkingSpace.user_id == user_id).one()
            entity = CheckOutParkingSpaceMapper.to_entity(record=parking_space)
            raise Return(entity)

    @classmethod
    @coroutine
    def upsert(cls, parking_space):
        """

        Update/Insert parking space, if user already have parking space, update user's information
        otherwise, insert a new parking space, and parking_space have to be a ParkingSpace entity
        with all required fields

        :param ParkingSpace parking_space:
        :return ParkingSpace:
        :raises AssertionError: the parking_space provided doesn't have user_id
        :raises ValidationError: the parking_space provided missing required fields
        """
        assert parking_space.user_id
        parking_space.validate()

        try:
            _parking_space = yield cls._update(
                parking_space=parking_space,
                latitude=parking_space.latitude,
                longitude=parking_space.longitude,
                created_at=parking_space.create_at,
                level=parking_space.level,
                description=parking_space.description
            )
            raise Return(_parking_space)
        except NoResultFound:
            _parking_space = yield cls._insert(parking_space)
            raise Return(_parking_space)

    @staticmethod
    @coroutine
    def remove(user_id):
        """
        Remove a parking_space using user_id

        :param str user_id:
        :return ParkingSpace: deleted parking space
        """
        with create_session() as session:
            rows = session.query(CheckOutParkingSpace).filter(
                CheckOutParkingSpace.user_id == user_id
            ).delete()
            if rows == 0:
                raise NoResultFound

            raise Return(rows)

    @classmethod
    @coroutine
    def _update(cls,
                parking_space,
                latitude,
                longitude,
                created_at,
                level,
                description):
        """

        :param ParkingSpace parking_space:
        :return ParkingSpace:
        """
        with create_session() as session:
            _parking_space = session.query(CheckOutParkingSpace).filter(
                CheckOutParkingSpace.user_id == parking_space.user_id
            ).one()

            _parking_space.latitude = latitude
            _parking_space.longitude = longitude
            _parking_space.created_at = created_at

            if level:
                _parking_space.level = level
            if description:
                _parking_space.description = description

            entity = CheckOutParkingSpaceMapper.to_entity(record=_parking_space)

            raise Return(entity)

    @classmethod
    @coroutine
    def _insert(cls, parking_space):
        """
        Insert a new parking_space into db

        :param ParkingSpace parking_space:
        :return ParkingSpace: Inserted parking_space
        """
        with create_session() as session:
            _parking_space = CheckOutParkingSpaceMapper.to_model(parking_space)
            session.add(_parking_space)
            raise Return(parking_space)


class ParkingSpaceNotFound(NotFound):
    error = 'Parking Space Not Found'