from tornado.gen import coroutine


class WaitingUserPool(object):

    @coroutine
    def read_one(self, user_id):
        """
        Return a waiting user by user_id
        :param user_id:
        :return: WaitingUser
        :raise NoResultFound: user is not in the pool
        """
        pass

    @coroutine
    def read_many(self, location):
        """
        This method will return all the users in certain (*range) according to given
        coordinate or location
        (*range) is defined in config file ('MatchingAlgorithm.range')

        :return:
        """
        pass

    @coroutine
    def insert(self, waiting_user):
        """
        Insert a new waiting user into pool

        :param WaitingUser waiting_user:
        :return:
        """
        pass

    @coroutine
    def update(self, user_id, is_active):
        """
        Update the status(is_active) of the user with given user_id

        :return WaitingUser:
        :param user_id:
        :param is_active:
        :return:
        :raises NoResultFound: use is not in the pool
        """
        pass

    @coroutine
    def remove(self, user_id):
        """
        remove a user row from a user waitting pool
        :param user_id:
        :return:
        """

        pass

    @coroutine
    def pop_one(self, longitude, latitude, location, ignore_user_ids=None, _ranking=None):
        """
        This method will
            1. read len(ignore_user_ids) +1 active users
            2. rank them with _ranking method if it is provided
            3. and get first user
            4. update the status of this user as inactive
            5. return the user

        :param float longitude:
        :param float latitude:
        :param float location:
        :param list<string> ignore_user_ids: list of user_id that want to be filtered out
        :param func _ranking: ranking algorithm
        :return WaitingUser:
        :raises NoResultFound: no waiting user in given coordinate
        """

        pass
