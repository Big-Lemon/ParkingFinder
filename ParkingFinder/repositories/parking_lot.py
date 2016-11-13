from tornado.gen import coroutine


class ParkingLotRepository(object):

    @coroutine
    def read_one(self, plate):
        """
        Read one by plate

        :param str plate:
        :return:
        :raises noResultFound: vehicle with given plate is not in the parking lot
        """
        pass

    @coroutine
    def read_many(self):
        """
        Read many by user_id

        :return:
        """
        pass

    @coroutine
    def insert(self, parking_space):
        """
        Insert a parking space to the parking lot

        :return ParkingSpace:
        """
        pass

    @coroutine
    def remove(self, plate):
        """
        Remove a parking space by the plate from parking lot

        :return:
        """
        pass
