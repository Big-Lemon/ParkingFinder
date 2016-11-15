from clay import config
from sqlalchemy.orm.exc import NoResultFound
from tornado.gen import coroutine, Return

from ParkingFinder.base.errors import BaseError, NotFound
from ParkingFinder.base.with_repeat import Timeout, ReachRepeatLimit
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


class UserRequestService(object):

    @classmethod
    @with_repeat(
        repeat_exceptions=ReultFoundInUserWaitingPool,
        repeat_times=awaiting_matching_repeat_times,
        timeout=awaiting_matching_time_out,
        duration=awaiting_matching_duration,
    )
    @coroutine
    def request_parking_space(cls, waiting_user):
        """
        service that handles user's parking space request

        :param: cached_space_list: list of previous user-rejected parking_plate_number
        :param: waiting_user: user entity
        :raise: Timeout: no space is available in a specific time so return timeout->
        :return: List<ParkingSpace>
        """
        try:
            list_of_matched_space = yield MatchedParkingList.read_many(waiting_user.user_id)
            spaces_return = []
            for matching_space in list_of_matched_space:
                space = yield ParkingLotRepository.read_one(matching_space.plate)
                spaces_return.append(space)
            raise Return(spaces_return)
        except NoResultFound:
            try:
                user_info = yield WaitingUserPool.read_one(waiting_user.user_id)
                raise ReultFoundInUserWaitingPool
            except NoResultFound:
                yield WaitingUserPool.insert(waiting_user)
                try:
                    list_of_available_space = yield AvailableParkingSpacePool.read_many(waiting_user.latitude,
                                                                                        waiting_user.longitude)
                    i = 0
                    spaces_return = []
                    while i < len(list_of_available_space):
                        # mark user as inactive here
                        yield AvailableParkingSpacePool.update(list_of_available_space[i].plate, False)
                        space = yield ParkingLotRepository.read_one(list_of_available_space[i].plate)
                        # insert matched result in the Pre_reserved table and mark status as awaiting
                        MatchedParkingList.insert(
                            MatchedParkingSpace({
                                'plate': space.plate,
                                'user_id': waiting_user.user_id,
                                'status': 'awaiting',
                            })
                        )
                        spaces_return.append(space)
                        i += 1
                    raise Return(spaces_return)
                except NoResultFound:
                    yield WaitingUserPool.update(waiting_user.user_id, True)

    @classmethod
    @coroutine
    def accept_parking_space(cls, user_id, accepted_space_plate):
        """
        service that handles user's accepting parking case
        :param: user_id:
        :param: accepted_space_plates: can be one or null. if it is null it means user rejects
                all the spaces we provide
        :raise: TimeOut: use didn't make choice in a specific time range
        :return: Token: the real_time token
        """
        try:
            list_of_matching_space = yield MatchedParkingList.read_many(user_id)
            # loop to change the corresponding status in the table
            for matched_result in list_of_matching_space:
                if accepted_space_plate != matched_result.plate:
                    yield MatchedParkingList.update(user_id, matched_result.plate, 'rejected')
                elif matched_result.is_expired():
                    yield MatchedParkingList.update(user_id, matched_result.plate, 'expired')
                    raise Timeout
                else:
                    yield MatchedParkingList.update(user_id, matched_result.plate, 'reserved')
            yield WaitingUserPool.remove(user_id)
            real_time_location = yield RealTimeLocationService.fetch_real_time_location(
                token=accepted_space_plate
            )
            raise Return(real_time_location)
        except NoResultFound:
            raise Timeout



    @classmethod
    @coroutine
    def reject_all_parking(cls, user_id, is_continue_service):
        """
        service that handles user's rejecting parking case
        :param user_id:
        :param is_continue_service:
        :raise NoResultFound: tell handler that put this guy into requesting again
        :return:
        """
        try:
            list_of_matching_space = yield MatchedParkingList.read_many(user_id)
            for matched_result in list_of_matching_space:
                yield MatchedParkingList.update(user_id, matched_result.plate, 'rejected')
            if not is_continue_service:
                yield WaitingUserPool.remove(user_id)
            else:
                raise NoResultFound
        except NoResultFound:
            if is_continue_service:
                raise NoResultFound
            else:
                yield WaitingUserPool.remove(user_id)

    @classmethod
    @coroutine
    def fetching_space_nearby(cls, latitude, longitude):
        """
        fetch the space that is near the location
        :param latitude:
        :param longitude:
        :raise NNoResultFound
        :return: List<ParkingSpace>
        """
        try:
            list_of_avialable_space = yield AvailableParkingSpacePool.read_many(latitude=latitude, longitude=longitude)
            space_return = []
            for available_space in list_of_avialable_space:
                space = yield ParkingLotRepository.read_one(available_space.plate)
                space_return.append(space)
            raise Return(space_return)
        except NoResultFound:
            raise NoResultFound



class ReultFoundInUserWaitingPool(BaseError):
    pass


