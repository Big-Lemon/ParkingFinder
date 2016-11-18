from sqlalchemy.orm.exc import NoResultFound
from tornado.gen import coroutine, Return

from ParkingFinder.base.async_db import create_session
from ParkingFinder.base.errors import NotFound
from ParkingFinder.mappers.available_parking_space_mapper import AvailableParkingSpaceMapper
from ParkingFinder.tables.available_parking_space_pool import AvailableParkingSpacePool as Pool

class AvailableParkingSpacePool(object):

    @staticmethod
    @coroutine
    def read_one(plate):
        """
        Read one parking space by plate

        :param str plate: plate of vehicle that holds the parking space
        :return AvailableParkingSpace:
        :raises NoResultFound: the vehicle with given plate hasn't been posted yet
        """
        with create_session() as session:
            parking_space = session.query(Pool).filter(
                Pool.plate == plate
            ).one()
            entity = AvailableParkingSpaceMapper.to_entity(record=parking_space)
            raise Return()

    @staticmethod
    @coroutine
    def read_many(
            longitude=None,
            latitude=None,
            location=None,
    ):
        """
        Read all parking spaces within certain (*range) corresponding to
        the 'coordinate' or in location
        (*range) is defined in config file ('matching_algorithm.range')

        *****return only active ones******

        :param float longitude:
        :param float latitude:
        :param str location:
        :raises NoResultFound: no active parking space available for certain range
        :return List<AvailableParkingSpace>:
        """
        assert (longitude and latitude) or location
        pass

    @classmethod
    @coroutine
    def insert(cls, available_parking_space):
        """
        Insert a new available parking space into pool

        :param AvailableParkingSpace available_parking_space:
        :return AvailableParkingSpace:
        """
        with create_session() as session:
            #available_parking_space.validate()
            _available_parking_space = AvailableParkingSpaceMapper.to_model(available_parking_space)
            session.add(_available_parking_space)
            raise Return(available_parking_space)
        pass

    @classmethod
    @coroutine
    def update(cls, plate, is_active):
        """
        Update 'is_active' column of a parking space with given plate
        :param str plate:
        :param boolean is_active:
        :return AvailableParkingSpace:
        """
        pass

    @classmethod
    @coroutine
    def remove(cls, plate):
        """
        Remove a available parking space by plate
        :param str plate:
        :return AvailableParkingSpace:
        """
        pass

    @classmethod
    @coroutine
    def pop_many(cls, longitude, latitude, location, _filter=None):
        """
        This method will find (#) of parking spaces within certain (*range)
        that can be passed by '_filter'
        (#) is defined in config ('matching_algorithm.nParkingReturn')
        (*range) is defined in config ('matching_algorithm.range')
        part of differences between this one and read many is that this one will
        update the status as inactive as they are fetched out

        :param float longitude:
        :param float latitude:
        :param str location:
        :param func _filter:
        :return list<AvailableParkingSpace>:
        """
        pass
