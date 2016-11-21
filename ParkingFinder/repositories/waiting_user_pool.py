import redis as _redis
from clay import config
from sqlalchemy.orm.exc import NoResultFound
from tornado.gen import coroutine, Return

from ParkingFinder.base.redis_pool import redis_pool
from ParkingFinder.mappers.waiting_user_mapper import WaitingUserMapper

logger = config.get_logger('handler.waiting_user_pool')

WAITING_USER = 'waiting_user:'
COORDINATE = 'active_waiting_user:'


class WaitingUserPool(object):
    @classmethod
    @coroutine
    def read_one(cls, user_id):
        """
        Return a waiting user by user_id
        :param user_id:
        :return: WaitingUser
        :raise NoResultFound: user is not in the pool
        """
        assert user_id
        redis = _redis.StrictRedis(connection_pool=redis_pool)
        try:
            if not redis.exists(WAITING_USER + user_id):
                raise NoResultFound
            record = redis.hgetall(WAITING_USER + user_id)
            try:
                coordinate = redis.geopos(COORDINATE, user_id)
            except TypeError:
                coordinate = []

            if coordinate:
                record['is_active'] = True
            else:
                record['is_active'] = False
            entity = WaitingUserMapper.to_entity(record=record)
            raise Return(entity)
        except TypeError:
            raise NoResultFound

    @classmethod
    @coroutine
    def read_many(cls, location):
        """
        This method will return all the users in certain (*range) according to given
        coordinate or location
        (*range) is defined in config file ('MatchingAlgorithm.range')

        :return:
        """
        raise NotImplemented

    @classmethod
    @coroutine
    def insert(cls, waiting_user):
        """
        Insert a new waiting user into pool

        :param WaitingUser waiting_user:
        :return:
        """
        waiting_user.validate()
        redis = _redis.StrictRedis(connection_pool=redis_pool)
        redis.hmset(
            WAITING_USER + waiting_user.user_id,
            WaitingUserMapper.to_record(entity=waiting_user)
        )
        logger.info({
            'message': 'new user has been inserted into waiting pool',
            'user': waiting_user
        })
        if waiting_user.is_active:
            redis.geoadd(
                COORDINATE,
                waiting_user.location.longitude,
                waiting_user.location.latitude,
                waiting_user.user_id
            )
            logger.info({
                'message': 'user has been marked as active',
                'user': waiting_user
            })
        else:
            redis.zrem(COORDINATE, waiting_user.user_id)
            logger.info({
                'message': 'user has been marked as inactive',
                'user': waiting_user
            })
        raise Return(waiting_user)

    @classmethod
    @coroutine
    def update(cls, user_id, is_active=None, location=None):
        """
        Update the status(is_active) of the user with given user_id

        :return WaitingUser:
        :param user_id:
        :param is_active:
        :param location:
        :return:
        :raises NoResultFound: use is not in the pool
        """
        assert is_active != None or location
        redis = _redis.StrictRedis(connection_pool=redis_pool)
        try:
            if location:
                location.validate()
                if not redis.exists(
                    WAITING_USER + user_id
                ):
                    raise NoResultFound
                redis.hmset(
                    WAITING_USER + user_id,
                    {
                        'latitude': location.latitude,
                        'longitude': location.longitude,
                    }
                )
            if is_active:
                _latitude = redis.hget(
                    WAITING_USER + user_id,
                    'latitude'
                )
                _longitude = redis.hget(
                    WAITING_USER + user_id,
                    'longitude'
                )
                redis.geoadd(
                    COORDINATE,
                    _longitude,
                    _latitude,
                    user_id
                )
                logger.info({
                    'message': 'user status switch to active',
                    'user': {
                        'user_id': user_id,
                        'is_active': is_active
                    }
                })
            else:
                redis.zrem(COORDINATE, user_id)
                logger.info({
                    'message': 'user status switch to inactive',
                    'user': {
                        'user_id': user_id,
                        'is_active': is_active
                    }
                })
            waiting_user = yield cls.read_one(user_id=user_id)
            raise Return(waiting_user)
        except TypeError:
            raise NoResultFound

    @classmethod
    @coroutine
    def remove(cls, user_id):
        """
        remove a user row from a user waitting pool
        :param user_id:
        :return WaitingUser:
        :raise NoResultFound:
        """
        waiting_user = yield cls.read_one(user_id=user_id)
        redis = _redis.StrictRedis(connection_pool=redis_pool)
        if not redis.exists(WAITING_USER + user_id):
            raise NoResultFound
        redis.zrem(COORDINATE, user_id)
        redis.delete(WAITING_USER + user_id)
        logger.info({
            'message': 'user removed from waiting pool',
            'user': waiting_user
        })
        raise Return(waiting_user)

    @classmethod
    @coroutine
    def pop_one(cls, longitude, latitude, location=None, ignore_user_ids=None, _ranking=None):
        """
        This method will
            1. read len(ignore_user_ids) +1 active users
            2. rank them with _ranking method if it is provided
            3. and get first user
            4. update the status of this user as inactive
            5. return the user

        :param float longitude:
        :param float latitude:
        :param list<string> ignore_user_ids: list of user_id that want to be filtered out
        :param func _ranking: ranking algorithm
        :return WaitingUser:
        :return None: no waiting user in given coordinate
        """
        assert (longitude and latitude)
        radius = config.get('matching.radius')
        unit = config.get('matching.unit')
        _ignore_user_ids = set(ignore_user_ids or [])

        redis = _redis.StrictRedis(connection_pool=redis_pool)
        with redis.pipeline() as pipeline:
            while 1:
                try:
                    pipeline.watch(COORDINATE)
                    waiting_users = pipeline.georadius(
                        name=COORDINATE,
                        longitude=longitude,
                        latitude=latitude,
                        radius=radius,
                        unit=unit,
                        sort='ASC'
                    )
                    logger.info({
                        'message': 'waiting users in the area',
                        'waiting_users': waiting_users,
                        'latitude': latitude,
                        'longitude': longitude,
                        'radius': radius,
                        'unit': unit
                    })
                    for user in waiting_users:
                        if user not in _ignore_user_ids:
                            pipeline.zrem(COORDINATE, user)
                            # back to buffered mode
                            pipeline.multi()
                            record = redis.hgetall(WAITING_USER + user)
                            record['is_active'] = False
                            entity = WaitingUserMapper.to_entity(record)
                            # commit
                            pipeline.execute()
                            logger.info({
                                'message': 'user has been matched with a vehicle',
                                'user': entity
                            })
                            raise Return(entity)
                    raise Return(None)
                except _redis.WatchError:
                    pass

        raise NoResultFound
