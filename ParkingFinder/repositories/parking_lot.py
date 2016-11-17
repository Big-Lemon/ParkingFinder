from tornado.gen import coroutine, Return


class ParkingLotRepository(object):

    @classmethod
    @coroutine
    def read_one(cls, plate):
        """
        Read one by plate

        :param str plate:
        :return: <ParkingSpace>:
        :raises noResultFound: vehicle with given plate is not in the parking lot
        """
        
        raise Return()

    @classmethod
    @coroutine
    def read_many(cls, plates):
        """
        Read many by a list of plates
        :param plates: list<plates>
        :raises noResultFound: vehicle with given plate is not in the parking lot
        :return: list<ParkingSpace>
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
