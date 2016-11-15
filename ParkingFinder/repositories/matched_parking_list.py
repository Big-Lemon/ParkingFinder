from tornado.gen import coroutine


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
        pass

    @classmethod
    @coroutine
    def read_many(cls, user_id):
        """
        Read many by user id

        :param str user_id:
        :return list<MatchedParkingSpace>:
        """
        pass

    @staticmethod
    @coroutine
    def insert(matched_parking_space):
        """
        Insert a matched parking space with waiting user into the list
        :param MatchedParkingSpace matched_parking_space:
        :return MatchedParkingSpace:
        """
        pass

    @classmethod
    @coroutine
    def remove(cls, plate):
        """
        Remove a matched Parking Space from the list

        :param str plate:
        :return MatchedParkingSpace:
        """
        pass
