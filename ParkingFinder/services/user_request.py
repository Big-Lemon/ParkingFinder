from tornado.gen import coroutine, Return


class UserRequestService(object):

    @classmethod
    @coroutine
    def fetch_list_of_parking_space(cls, waiting_user):
        """
        fetch list of available parking space entities (current maximum space is 2 spaces )
        if first fetch has space in pool
            do not put the user into user_waiting_table
            mark those space from parking_space_pool table as inactive
            add them to pre_reserved_parking_space table and mark all of them as waiting status
            return list of those available parking space
        else (first fetch has no space in pool )
            put the user into user_waiting_table
            and doing a loop here to check until user is assigned a space in pre_reserved_space table
            return a list of that assigned space


        :param: waiting_user: waiting_user entity
        :return: List[AvailableSpace]
        """

    @classmethod
    @coroutine
    def space_choice(cls, accepted_space_plate, non_accepted_space_plates):
        """
        Here returns the list of spaces that user rejects and only plate number is needed since plate number
        can uniquely identify a row in pre_reserved_space table. All of those rows indicated in this list will
        be removed from pre_reserved_parking_space table and added back to parking_space_pool table

        if the accepted_space_plate is null
            we do nothing return null
        if it is not null
            then mark the row in pre_reserved_parking_space as reserved for waiting user to check
            then also check to see if this user in the user_waiting_table, if so delete that user
            from the waiting_user table. call the real_time_handling function to start real time service
            return a realTime entity

        pre_reserved_parking_space deletion and parking_space_pool deletion will bot be handled here



        :param: accepted_space_plates: can be one or null. if it is null it means user rejects all the spaces
                we provide
        :param: non_accepted_space_plates: list of spaces that user rejects
        :return: RealTime: the real_time entity
        """

    @classmethod
    @coroutine
    def _real_time_handling(cls, user_id):
        """
        a function to initiate a real_time location service in requesting user side
        :return: RealTime: the real_time entity
        """



