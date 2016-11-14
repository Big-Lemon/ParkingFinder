from tornado.gen import coroutine, Return


class UserRequestService(object):

    @classmethod
    @coroutine
    def request_parking_space(cls, waiting_user, cached_space_list):
        """
        service that handles user's parking space request

        :param: cached_space_list: list of previous user-rejected parking_plate_number
        :param: waiting_user: user entity
        :return: List[AvailableSpace]
        """
        """
        pseudo-code:
        timestamp time = current time
        list_of_space = matching_parking_space_repository.readList()(should return list of matching_space_entity
                                                                    or null)
        while()
        """

    @classmethod
    @coroutine
    def accept_parking_space(cls, user_id, accepted_space_plate):
        """
        service that handles user's accepting parking case
        :param: user_id:
        :param: accepted_space_plates: can be one or null. if it is null it means user rejects
                all the spaces we provide
        :return: RealTime: the real_time entity or null
        """

    @classmethod
    @coroutine
    def reject_all_parking(cls, user_id):
        """
        service that handles user's rejecting parking case
        :param user_id:
        :return:
        """

    @classmethod
    @coroutine
    def _real_time_handling(cls, user_id, plate):
        """
        a function to initiate a real_time location service in accepted user side
        :return: RealTime: the real_time entity
        """



