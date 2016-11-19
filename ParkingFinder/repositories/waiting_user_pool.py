from clay import config
from sqlalchemy.orm.exc import NoResultFound
from tornado.gen import coroutine, Return
from math import sqrt

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
        pass

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
        pass

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
        pass

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


            sorted(_ignore_user_ids)
            if _waiting_users == None:
                raise NoResultFound

            #sorted by distance
            _waiting_users = sorted(_waiting_users, key=lambda e: cls.distance(e, longitude, latitude))
            
            for user in _waiting_users:
                if user.user_id not in _ignore_user_ids:
                    user.is_active = False
                raise Return(user)

    @staticmethod
    def distance(waiting_users, longitude, latitude):
        return sqrt((float(waiting_users.longitude) - longitude)**2 + (float(waiting_users.latitude) - latitude)**2)
