from tornado.gen import coroutine


class MatchedParkingList(object):

    @coroutine
    def read_one(self, plate):
        """
        Read one by plate

        :param str plate:
        :return MatchedParkingSpace:
        :raises vehicle with given plate doesn't have matched waiting user
        """
        pass

    @coroutine
    def read_many(self, user_id):
        """
        Read many and only return list<MatchedParkingSpace> such that every
        MatchedParkingSpace inside with status "waiting"

        :param str user_id:
        :raise: NoResultFound:
        :return list<MatchedParkingSpace>:
        """
        pass

    @coroutine
    def update(self, user_id, plate, status):
        """
        Update status column of a matched_result with given combination of user_id and plate
        :param str user_id:
        :param str plate:
        :param string status:

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

    @coroutine
    def remove(self, plate):
        """
        Remove a matched Parking Space from the list

        :param str plate:
        :return MatchedParkingSpace:
        """
        pass
