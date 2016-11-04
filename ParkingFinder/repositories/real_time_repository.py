from sqlalchemy.orm.exc import NoResultFound
from tornado.gen import coroutine, Return

from ParkingFinder.base.async_db import create_session
from ParkingFinder.base.errors import NotFound
from ParkingFinder.mappers.real_time_mapper import RealTimeMapper
from ParkingFinder.tables.real_time import RealTimes


class RealTimeRepository(object):

    @staticmethod
    @coroutine
    def read_one(user_id):
        """
        Read from realtime with user_id 

        :param str key:
        :return data:
        :raises sqlalchemy.orm.exc.NoResultFound:
        """
        with create_session() as session:
            realtime = session.query(RealTimes).filter(
                RealTimes.waiting_user_id == user_id
            ).one()
            entity = RealTimeMapper.to_entity(record=realtime)
            raise Return(entity)

    @classmethod
    @coroutine
    def upsert(cls, user_id, realtime):
        """
        Update/Insert realtime, if realtime exist, update realtime's information
        otherwise, insert a new realtime, and realtime have to be a realtime entity
        with all required fields

        :param RealTime realtime:
        :return RealTime:
        :raises AssertionError: the user provided doesn't have user_id
        :raises ValidationError: the user provided missing required fields
        """

        try:
            _realtime = yield cls._update(user_id, realtime)
            raise Return(_realtime)

        except NoResultFound:
            _realtime = yield cls._insert(realtime)
            raise Return(_realtime)

    @classmethod
    @coroutine
    def _update(cls,
                user_id,
                realtime
                ):
        """

        :param str user_id:
        :param Realtime realtime:
        :return RealTime: updated RealTime
        :raises NoResultFound: the realtime that is requested to update is not exist
        """

        with create_session() as session:
            _realtime = session.query(RealTimes).filter(
                RealTimes.waiting_user_id == realtime.waiting_user_id
            ).one()
            if user_id == realtime.request_user_id:
                _realtime.request_user_latitude = realtime.request_user_latitude
                _realtime.request_user_longitude = realtime.request_user_longitude
            else:
                _realtime.waiting_user_latitude = realtime.waiting_user_latitude
                _realtime.waiting_user_longitude = realtime.waiting_user_longitude

            entity = RealTimeMapper.to_entity(_realtime)

            raise Return(entity)

    @staticmethod
    @coroutine
    def _insert(realtime):
        """
        Insert a new real time into db

        :param realtime realtime: complete entity will all required fields
        :return realtime: realtime
        """
        with create_session() as session:
            realtime.validate()
            _realtime = RealTimeMapper.to_model(realtime)
            session.add(_realtime)
            raise Return(realtime)


class KeyNotFound(NotFound):
    error = 'Key Not Found'
