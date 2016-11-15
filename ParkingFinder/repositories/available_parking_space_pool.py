from tornado.gen import coroutine


class AvailableParkingSpacePool(object):

    @coroutine
    def read_one(self, plate):
        """
        Read one parking space by plate

        :param str plate: plate of vehicle that holds the parking space
        :return AvailableParkingSpace:
        :raises NoResultFound: the vehicle with given plate hasn't been posted yet
        """
        pass

    @staticmethod
    @coroutine
    def read_many(
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
        pass

    @coroutine
    def insert(self, available_parking_space):
        """
        Insert a new available parking space into pool

        :param AvailableParkingSpace available_parking_space:
        :return AvailableParkingSpace:
        """
        pass

    @coroutine
    def update(self, plate, is_active):
        """
        Update 'is_active' column of a parking space with given plate
        :param str plate:
        :param boolean is_active:
        :return AvailableParkingSpace:
        """
        pass

    @coroutine
    def remove(self, plate):
        """
        Remove a available parking space by plate
        :param str plate:
        :return AvailableParkingSpace:
        """
        pass

    @coroutine
    def pop_many(self, longitude, latitude, location, _filter=None):
        """
        This method will find (#) of parking spaces within certain (*range)
        that can be passed by '_filter'
        (#) is defined in config ('matching_algorithm.nParkingReturn')
        (*range) is defined in config ('matching_algorithm.range')

        :param float longitude:
        :param float latitude:
        :param str location:
        :param func _filter:
        :return list<AvailableParkingSpace>:
        """
        pass
