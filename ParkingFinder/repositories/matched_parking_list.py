from clay import config
from tornado.gen import coroutine, Return
from sqlalchemy.orm.exc import NoResultFound

from ParkingFinder.base.async_db import create_session
from ParkingFinder.mappers.matched_parking_space_mapper import MatchedParkingSpaceMapper
from ParkingFinder.tables.matched_parking_space_list import MatchedParkingSpaceList


class MatchedParkingList(object):

    @classmethod
    @coroutine
    def read_one(cls, plate):
        """
        Read one by plate
        :param str plate:
        :return MatchedParkingSpace:
        :raises vehicle with given plate doesn't have matched waiting user
        """
        with create_session() as session:
            matched_parking_list = session.query(MatchedParkingSpaceList).filter(
                MatchedParkingSpaceList.plate == plate
            ).one()
            entity = MatchedParkingSpaceMapper.to_entity(record=matched_parking_list)

            raise Return(entity)

    @classmethod
    @coroutine
    def read_many(cls, user_id):
        """
        Read many and only return list<MatchedParkingSpace>

        :param str user_id:
        :return list<MatchedParkingSpace>:
        """

        with create_session() as session:
            matched_parking_list = session.query(MatchedParkingSpaceList).filter(
                MatchedParkingSpaceList.user_id == user_id
            ).all()
            entities = [
                MatchedParkingSpaceMapper.to_entity(record=matched_parking)
                for matched_parking in matched_parking_list
                ]

            raise Return(entities)

    @classmethod
    @coroutine
    def update(cls, user_id, plate, status):
        """
        Update status column of a matched_result with given combination of user_id and plate
        :param str user_id:
        :param str plate:
        :param string status:
        """

        with create_session() as session:
            matched_parking_list = session.query(MatchedParkingSpaceList).filter(
                MatchedParkingSpaceList.plate == plate
            ).one()
            matched_parking_list.status = status
            entity = MatchedParkingSpaceMapper.to_entity(record=matched_parking_list)
            raise Return(entity)

    @staticmethod
    @coroutine
    def insert(matched_parking_space):
        """
        Insert a matched parking space with waiting user into the list
        :param MatchedParkingSpace matched_parking_space:
        :return MatchedParkingSpace:
        """

        with create_session() as session:
            matched_parking_space.validate()
            _matched_parking_space = MatchedParkingSpaceMapper.to_model(matched_parking_space)
            session.add(_matched_parking_space)

            raise Return(matched_parking_space)

    @classmethod
    @coroutine
    def remove(cls, plate):
        """
        Remove a matched Parking Space from the list
        :param str plate:
        :return MatchedParkingSpace:
        """
        with create_session() as session:
            matched_parking_space = session.query(MatchedParkingSpaceList).filter(
                MatchedParkingSpaceList.plate == plate
            ).one()
            entity = MatchedParkingSpaceMapper.to_entity(matched_parking_space)
            session.query(MatchedParkingSpaceList).filter(
                MatchedParkingSpaceList.plate == plate
            ).delete()
            raise Return(entity)

