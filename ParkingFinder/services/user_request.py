from clay import config
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from tornado.gen import coroutine, Return

from ParkingFinder.base.errors import BaseError, NotFound, InvalidEntity, InvalidArguments
from ParkingFinder.base.errors import Timeout
from ParkingFinder.base.with_repeat import with_repeat
from ParkingFinder.repositories import (
    AvailableParkingSpacePool,
    MatchedParkingList,
    ParkingLotRepository,
    WaitingUserPool,
)
from ParkingFinder.entities.matched_parking_space import MatchedParkingSpace
from ParkingFinder.services.real_time_location_service import RealTimeLocationService

logger = config.get_logger('service.parking_space')

awaiting_matching_time_out = config.get('matching.matching_timeout')
awaiting_matching_duration = config.get('matching.matching_duration')
awaiting_matching_repeat_times = config.get('matching.matching_repeat_times')
awaiting_action_time_out = config.get('matching.awaiting_action_timeout')
awaiting_action_duration = config.get('matching.awaiting_action_duration')
awaiting_action_repeat_times = config.get('matching.awaiting_action_repeat_times')

# now available_parking_space has longi lati loc and plate return available_space_list enough
# use pop_many instead of read_many
# insert -> exception, read-> notFoundException, update-> # of rows affected,  remove -> none -> remove fail


class NoResultFoundInMatchedSpaceTable(BaseError):
    error = "No Result found In Matched Space Table"


class CanNotStopForwardingMessage(BaseError):
    error = "Can Not Forwarding Message"


class UserRequestService(object):

    @classmethod
    @coroutine
    def request_parking_space(cls, waiting_user):
        """
        service that handles user's parking space request

        :param: cached_space_list: list of previous user-rejected parking_plate_number
        :param: waiting_user: user entity
        :raise: Timeout: no space is available in a specific time so return timeout
        :raise InvalidArgument: means user terminates further service
        :raise InvalidEntity: the user passed in is not valid
        :return: List<AvailableParkingSpace>
        """
        # branch to handle fetching list of available spaces
        space_return = []
        try:
            user_info = yield WaitingUserPool.read_one(user_id=waiting_user.user_id)
            # TODO if user exist, update user geographical location
            try:
                space_return = yield cls._loop_checking_space_availability(user_id=waiting_user.user_id)
            except Timeout:
                pass
        except NoResultFound:
            try:
                inserted_user = yield WaitingUserPool.insert(waiting_user=waiting_user)
            except IntegrityError:
                raise InvalidEntity
            try:
                space_return = yield cls._checking_space_availability(waiting_user=waiting_user)
            except Timeout:
                pass

        # branch to handle if user continue to use the service
        try:
            # case where user continue the service

            user_info = yield WaitingUserPool.read_one(user_id=waiting_user.user_id)
            if not space_return:
                raise Timeout
            raise Return(space_return)
        except NoResultFound:
            # case where user stop the service
            for space in space_return:
                modified_row = yield MatchedParkingList.update(
                    user_id=waiting_user.user_id,
                    plate=space.plate,
                    status='rejected'
                )
                if modified_row == 0:
                    raise InvalidEntity
            raise InvalidArguments

    @classmethod
    @coroutine
    def accept_parking_space(cls, user_id, accepted_space_plate):
        """
        service that handles user's accepting parking case
        :param: str user_id:
        :param: accepted_space_plates: can be one or null. if it is null it means user rejects
                all the spaces we provide
        :raise: TimeOut: use didn't make choice in a specific time range
        :raise: InvalidEntity: this means information among tables is not consistent
                                possibly internal error
        :raise: InvalidArgument: this means user terminate the service in the half way
        :return: ParkingSpace: matched parking space
        """

        try:
            list_of_matching_space = yield MatchedParkingList.read_many(user_id=user_id)
            # loop to change the corresponding status in the table
            # import ipdb
            # ipdb.set_trace()
            for matched_result in list_of_matching_space:
                if accepted_space_plate != matched_result.plate:
                    _status = 'rejected'
                elif matched_result.is_expired:
                    _status = 'expired'
                    raise Timeout
                else:
                    _status = 'reserved'

                modified_row = yield MatchedParkingList.update(
                    user_id=user_id,
                    plate=matched_result.plate,
                    status=_status
                )
                if modified_row == 0:
                    raise InvalidEntity
                elif _status == 'expired':
                    raise Timeout

            removed = yield WaitingUserPool.remove(user_id=user_id)
            # case where user is not valid so we should mark that space as reject
            # and not return the token
            if not removed:
                yield MatchedParkingList.update(
                    user_id=user_id,
                    plate=accepted_space_plate,
                    status='rejected'
                )
                raise InvalidArguments
            else:
                parking_space = yield ParkingLotRepository.read_one(plate=accepted_space_plate)
                raise Return(parking_space)

        except NoResultFound:
            raise Timeout

    @classmethod
    @coroutine
    def reject_all_parking(cls, waiting_user):
        """
        service that handles user's rejecting parking case
        this function will either throw a exception or return a nonempty list
        :param WaitingUser waiting_user:
        :raise Timeout : means currently none of spaces can be found
        :raise InvalidArgument: means user terminates further service
        :raise InvalidEntity : this means information among tables is not consistent
                                possibly internal error
        :return: list<AvailableParkingSpace>
        """

        try:
            list_of_matching_space = yield MatchedParkingList.read_many(user_id=waiting_user.user_id)
            for matched_result in list_of_matching_space:
                modified_row = yield MatchedParkingList.update(user_id=waiting_user.user_id,
                                                               plate=matched_result.plate,
                                                               status='rejected')
                if modified_row == 0:
                    raise InvalidEntity
            # we also assume provide service first and then terminate if necessary to avoid inconsistency
        except NoResultFound:
            pass

        space_return = []
        try:
            space_return = yield cls._checking_space_availability(waiting_user=waiting_user)
        except Timeout:
            pass

        try:
            # case where user continue using the service
            user_existed = yield WaitingUserPool.read_one(user_id=waiting_user.user_id)
            if not space_return:
                raise Timeout
            raise Return(space_return)
        except NoResultFound:
            # case where user stop the service
            for space in space_return:
                modified_row = yield MatchedParkingList.update(user_id=waiting_user.user_id,
                                                               plate=space.plate,
                                                               status='rejected')
                if modified_row == 0:
                    raise InvalidEntity
            raise InvalidArguments

    @classmethod
    @coroutine
    def fetching_space_nearby(cls, latitude, longitude, location):
        """
        fetch the space that is near the location
        :param latitude:
        :param longitude:
        :param location
        :raise NNoResultFound
        :return: List<AvailableParkingSpace>
        """
        try:
            # you can only use read_many here since you don't want change the status of the space in table
            list_of_available_space = yield AvailableParkingSpacePool.read_many(latitude=latitude,
                                                                                longitude=longitude,
                                                                                location=location)
            space_return = list_of_available_space
            raise Return(space_return)
        except NoResultFound:
            raise NoResultFound

    @classmethod
    @with_repeat(
        repeat_exceptions=NoResultFoundInMatchedSpaceTable,
        repeat_times=awaiting_matching_repeat_times,
        timeout=awaiting_matching_time_out,
        duration=awaiting_matching_duration,
    )
    @coroutine
    def _loop_checking_space_availability(cls, user_id):
        """
        *** matched_parking_space_table == pre_reserved_table *****
        checking if there are spaces that are assigned to user in the
        matched_parking_space_table only and the result of this function will never
        return a empty list. Either timeout exception(in this case empty list) or
        list with spaces
        :param str user_id: this function only accept user that is
                                marked as "active "in the user waiting pool
        :raise Timeout
        :raise: InvalidEntity : this means information among tables is not consistent
                                possibly internal error
        :return: list<AvailableParkingSpace>
        """
        try:
            list_of_matched_space = yield MatchedParkingList.read_many(user_id=user_id)
            spaces_return = []
            for matching_space in list_of_matched_space:
                if matching_space.is_awaiting:
                    try:
                        space = yield AvailableParkingSpacePool.read_one(plate=matching_space.plate)
                        spaces_return.append(space)
                    except NoResultFound:
                        raise InvalidEntity
            if not spaces_return:
                raise NoResultFoundInMatchedSpaceTable
            else:
                raise Return(spaces_return)

        except NoResultFound:
            raise NoResultFoundInMatchedSpaceTable

    @classmethod
    @coroutine
    def _checking_space_availability(cls, waiting_user):
        """
        this function will first check the available available parking space pool
        if none is available then this will call the
        loop_checking_space_availability to find space by looping
        :param WaitingUser waiting_user: this function only accept user that is 
                                marked as "inactive " in the user waiting pool 
                                and possibly mark the user as "active" in the half 
                                way in order to call the 
                                loop_checking_space_availability. Inside logic has
                                enforced the consistency
        :raise Timeout
        :raise InvalidEntity : this means information among tables is not consistent
                                possibly internal error
        :return: list<AvailableParkingSpace>
        """
        # TODO: read_many API might change based on how the location value stored in each entity 
        # TODO: so parameter might change accordingly
        try:
            location = waiting_user.location
            list_of_available_space = yield AvailableParkingSpacePool.pop_many(latitude=location.latitude,
                                                                               longitude=location.longitude,
                                                                               location=location.location)
            spaces_return = list_of_available_space
            for space_element in list_of_available_space:
                # insert matched result in the Pre_reserved table and mark status as awaiting
                modified = yield MatchedParkingList.insert(
                    MatchedParkingSpace({
                        'plate': space_element.plate,
                        'user_id': waiting_user.user_id,
                        'status': 'awaiting',
                    })
                )
            raise Return(spaces_return)
        except IntegrityError:
            raise InvalidEntity
        except NoResultFound:
            # mark user as "active" here

            modified_row = yield WaitingUserPool.update(user_id=waiting_user.user_id, is_active=True)
            if modified_row == 0:
                raise InvalidEntity
            spaces_return = yield cls._loop_checking_space_availability(waiting_user.user_id)
            raise Return(spaces_return)

    @classmethod
    @coroutine
    def service_terminate(cls, user_id):
        """
        terminate the user service as requested
        :param str user_id:
        :raise CanNotStopForwardingMessage: this means either it is too late to terminate the service or
                                            there is a inconsistency exist in the table, possibly internal error
        :return:
        """
        removed = yield WaitingUserPool.remove(user_id=user_id)
        if not removed:
            raise CanNotStopForwardingMessage






