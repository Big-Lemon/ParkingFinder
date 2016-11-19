from clay import config
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
            raise Return(entity)

    @classmethod
    @coroutine
    def read_many(
            cls,
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
        radius = config.get('matching.radius')
        square_radius = radius * radius

        n = config.get('matching.num_display_parking_spaces')
        with create_session() as session:
            parking_spaces = session.query(Pool).filter(
                Pool.location == location or
                (
                    ((Pool.longitude - longitude) * (Pool.longitude - longitude)
                        + (Pool.latitude + latitude) * (Pool.latitude - latitude))
                    < square_radius
                )
            ).all()
            sorted(parking_spaces, key=lambda p: cls._distance(
                longitude=longitude,
                latitude=latitude,
                parking_space=p
            ))
            _parking_spaces = [AvailableParkingSpaceMapper.to_entity(parking_space)
                              for parking_space in parking_spaces[0:n]]
            raise Return(_parking_spaces)



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
    def pop_many(cls, longitude, latitude, location, ignore_list=None,_filter=None):
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
        assert (longitude and latitude) or location
        radius = config.get('matching.radius')
        square_radius = radius * radius
        _ignore_list = set(ignore_list or [])
        n = config.get('matching.num_display_parking_spaces')

        with create_session() as session:
            parking_spaces = session.query(Pool).filter(
                Pool.location == location or
                (
                    ((Pool.longitude - longitude) * (Pool.longitude - longitude)
                     + (Pool.latitude + latitude) * (Pool.latitude - latitude))
                    < square_radius
                )
            ).limit(len(_ignore_list) + n)

            sorted(parking_spaces, key=lambda p: cls._distance(
                longitude=longitude,
                latitude=latitude,
                parking_space=p
            ))
            count = 0
            _parking_spaces = []
            for parking_space in parking_spaces:
                if parking_space.plate not in _ignore_list:
                    parking_space.is_active = False
                    _parking_spaces.append(AvailableParkingSpaceMapper.to_entity(parking_space))
                    count += 1
                if count >= n:
                    break
            raise Return(_parking_spaces)

    @staticmethod
    def _distance(longitude, latitude, parking_space):
        x = abs(longitude - parking_space.longitude)
        y = abs(latitude- parking_space.latitude)
        return x * x + y * y

    @staticmethod
    def _is_in_range(longitude, latitude, parking_space):
        r = config.get('matching.radius')
        r = r * r
        x = abs(longitude - parking_space.longitude)
        y = abs(latitude- parking_space.latitude)
        return x * x + y * y < r