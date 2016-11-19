# coding=utf-8
from clay import config
from sqlalchemy.orm.exc import NoResultFound
from tornado.gen import coroutine, Return
from math import sqrt
from math import radians
from math import sin
from math import cos
from math import atan2

from ParkingFinder.base.async_db import create_session
from ParkingFinder.base.errors import NotFound
from ParkingFinder.mappers.waiting_user_mapper import WaitingUserMapper
from ParkingFinder.tables.waiting_users import WaitingUsers


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
        with create_session() as session:
            WaitingUser = session.query(WaitingUsers).filter(
                WaitingUsers.user_id == user_id
            ).one()
            entity = WaitingUserMapper.to_entity(record=user_id)
            raise Return(entity)

    @classmethod
    @coroutine
    def read_many(cls, location):
        """
        This method will return all the users in certain (*range) according to given
        coordinate or location
        (*range) is defined in config file ('MatchingAlgorithm.range')

        :return:
        """
        pass

    @classmethod
    @coroutine
    def insert(cls, waiting_user):
        """
        Insert a new waiting user into pool

        :param WaitingUser waiting_user:
        :return:
        """
        with create_session() as session:
            waiting_user.validate()
            _waiting_user = WaitingUserMapper.to_model(waiting_user)
            session.add(_waiting_user)
            raise Return(waiting_user)

    @classmethod
    @coroutine
    def update(cls, user_id, is_active):
        """
        Update the status(is_active) of the user with given user_id

        :return WaitingUser:
        :param user_id:
        :param is_active:
        :return:
        :raises NoResultFound: use is not in the pool
        """
        with create_session() as session:
            waiting_user = session.query(WaitingUsers).filter(
                WaitingUsers.user_id == user_id
            ).one()
            waiting_user.is_active = is_active
            entity = WaitingUserMapper.to_entity(record=waiting_user)
            raise Return(entity)

    @classmethod
    @coroutine
    def remove(cls, user_id):
        """
        remove a user row from a user waitting pool
        :param user_id:
        :return:
        """

        pass

    @classmethod
    @coroutine
    def pop_one(cls, longitude, latitude, ignore_user_ids=None, _ranking=None):
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
        :raises NoResultFound: no waiting user in given coordinate
        """
        assert (longitude and latitude)
        #radius = config.get('matching.radius')
        radius = 0;
        square_radius = radius * radius
        _ignore_user_ids = set(ignore_user_ids or [])

        with create_session() as session:
            _waiting_users = session.query(WaitingUsers).filter(
                WaitingUsers.is_active
            ).all()
            total = (len(_ignore_user_ids) + 2)


            _ignore_user_ids = sorted(_ignore_user_ids)
            if _waiting_users == None:
                raise NoResultFound

            #sorted by distance
            _waiting_users = sorted(_waiting_users, key=lambda u: cls._distance(u, longitude, latitude))
            
            for user in _waiting_users:
                if user.user_id not in _ignore_user_ids:
                    user.is_active = False
                raise Return(user)

    @staticmethod
    def _distance(waiting_user, longitude, latitude):
        """
        This function will
            use the ‘haversine’ formula to calculate the great-circle distance between
            two points – that is, the shortest distance over the earth’s surface – giving an
            ‘as-the-crow-flies’ distance between the points).
        :param waiting_user:
        :param longitude:
        :param latitude:
        :return: float distance(unit: m)
        """
        EARTH_RADIUS = 6371000
        phi1 = radians(waiting_user.location.latitude)
        phi2 = radians(latitude)
        delta_phi = radians(latitude - waiting_user.location.latitude)
        delta_lambda = radians(longitude - waiting_user.location.longitude)
        a = sin(delta_phi/2) * sin(delta_phi/2) + \
            cos(phi1) * cos(phi2) + \
            sin(delta_lambda/2) * sin(delta_lambda/2)
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        dist = EARTH_RADIUS * c
        return dist

