from tornado.gen import coroutine, Return


class ParkingLotRepository(object):

    @classmethod
    @coroutine
    def read_one(cls, plate):
        """
        Read one by plate

        :param str plate:
        :return:
        :raises noResultFound: vehicle with given plate is not in the parking lot
        """
        raise Return()

    @classmethod
    @coroutine
    def read_many(cls):
        """
        Read many by user_id

        :return:
        """
        raise NotImplemented

    @classmethod
    @coroutine
    def insert(cls, parking_space):
        """
        Insert a parking space to the parking lot

        :return ParkingSpace:
        """
        raise NotImplemented

    @classmethod
    @coroutine
    def remove(cls, plate):
        """
        Remove a parking space by the plate from parking lot

        :return:
        """
        raise NotImplemented
