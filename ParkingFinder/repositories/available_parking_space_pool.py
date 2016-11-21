import redis as _redis
from clay import config
from sqlalchemy.orm.exc import NoResultFound
from tornado.gen import coroutine, Return

from ParkingFinder.base.redis_pool import redis_pool
from ParkingFinder.entities.available_parking_space import AvailableParkingSpace
from ParkingFinder.mappers.available_parking_space_mapper import AvailableParkingSpaceMapper


AVAILABLE_PARKING = 'available_parking:'
COORDINATE = 'active_parking_coordinate:'


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
        assert plate
        redis = _redis.StrictRedis(connection_pool=redis_pool)
        try:
            if not redis.exists(AVAILABLE_PARKING + plate):
                raise NoResultFound

            parking = redis.hgetall(AVAILABLE_PARKING + plate)
            try:
                coordinate = redis.geopos(COORDINATE, plate)
            except TypeError:
                coordinate = []

            if coordinate:
                parking['is_active'] = True
            else:
                parking['is_active'] = False

            available_parking_space = AvailableParkingSpaceMapper.to_entity(parking)
            raise Return(available_parking_space)
        except TypeError:
            raise NoResultFound

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
        unit = config.get('matching.unit')

        redis = _redis.StrictRedis(connection_pool=redis_pool)
        available_parkings = redis.georadius(
            name=COORDINATE,
            longitude=longitude,
            latitude=latitude,
            radius=radius,
            unit=unit,
            withcoord=True,
            sort='ASC'
        )
        _entities = []
        for parking_space in available_parkings:
            record = redis.hgetall(AVAILABLE_PARKING + parking_space[0])
            record['is_active'] = True
            entity = AvailableParkingSpaceMapper.to_entity(record)
            entity.distance = parking_space[1]
            _entities.append(entity)

        raise Return(_entities)

    @classmethod
    @coroutine
    def insert(cls, available_parking_space):
        """
        Insert a new available parking space into pool

        :param AvailableParkingSpace available_parking_space:
        :return AvailableParkingSpace:
        """
        available_parking_space.validate()
        redis = _redis.StrictRedis(connection_pool=redis_pool)
        if available_parking_space.is_active:
            redis.geoadd(
                COORDINATE,
                available_parking_space.location.longitude,
                available_parking_space.location.latitude,
                available_parking_space.plate,
            )
        else:
            redis.zrem(COORDINATE, available_parking_space.plate)
        redis.hmset(
            AVAILABLE_PARKING + available_parking_space.plate,
            AvailableParkingSpaceMapper.to_record(entity=available_parking_space)
            )
        raise Return(available_parking_space)

    @classmethod
    @coroutine
    def update(cls, plate, is_active=None, location=None):
        """
        Update 'is_active' column of a parking space with given plate
        :param str plate:
        :param boolean is_active:
        :param Location location:
        :return AvailableParkingSpace:
        """
        assert location or is_active != None
        redis = _redis.StrictRedis(connection_pool=redis_pool)
        try:
            if location:
                location.validate()
                if not redis.exists(
                    AVAILABLE_PARKING + plate
                ):
                    raise NoResultFound
                redis.hmset(
                    AVAILABLE_PARKING + plate,
                    {
                        'latitude': location.latitude,
                        'longitude': location.longitude,
                    }
                )
            if not redis.exists(
                AVAILABLE_PARKING + plate
            ):
                raise NoResultFound
            if is_active:
                latitude = redis.hget(
                    AVAILABLE_PARKING + plate,
                    'latitude'
                )
                longitude = redis.hget(
                    AVAILABLE_PARKING + plate,
                    'longitude'
                )
                redis.geoadd(
                    COORDINATE,
                    longitude,
                    latitude,
                    plate,
                )
            else:
                redis.zrem(COORDINATE, plate)

            parking = yield cls.read_one(plate=plate)
            raise Return(parking)
        except TypeError:
            raise NoResultFound

    @classmethod
    @coroutine
    def remove(cls, plate):
        """
        Remove a available parking space by plate
        :param str plate:
        :return AvailableParkingSpace:
        :raise NoResultFound:
        """
        parking = yield cls.read_one(plate=plate)
        redis = _redis.StrictRedis(connection_pool=redis_pool)

        redis.zrem(COORDINATE, plate)
        if not redis.exists(AVAILABLE_PARKING + plate):
            raise NoResultFound
        redis.delete(AVAILABLE_PARKING + plate)
        raise Return(parking)

    @classmethod
    @coroutine
    def pop_many(cls, longitude, latitude, location=None, ignore_list=None,_filter=None):
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
        :param list<str> ignore_list: list of plate want to be ignored
        :return list<AvailableParkingSpace>:
        """
        assert (longitude and latitude)
        radius = config.get('matching.radius')
        unit = config.get('matching.unit')
        _ignore_list = set(ignore_list or [])
        n = config.get('matching.num_pop_parking_spaces')

        redis = _redis.StrictRedis(connection_pool=redis_pool)
        with redis.pipeline() as pipeline:
            while 1:
                try:
                    pipeline.watch(COORDINATE)
                    available_parkings = pipeline.georadius(
                        name=COORDINATE,
                        longitude=longitude,
                        latitude=latitude,
                        radius=radius,
                        unit=unit,
                        withdist=True,
                        sort='ASC'
                    )

                    _entities = []
                    for parking_space in available_parkings:
                        if parking_space[0] not in _ignore_list:
                            record = redis.hgetall(AVAILABLE_PARKING + parking_space[0])
                            # remove from active pool
                            pipeline.zrem(COORDINATE, parking_space[0])
                            record['is_active'] = False
                            record['distance'] = parking_space[1]
                            entity = AvailableParkingSpaceMapper.to_entity(record)
                            _entities.append(entity)
                            n -= 1
                        if n <= 0:
                            break
                    pipeline.execute()
                    raise Return(_entities)
                except _redis.WatchError:
                    pass

