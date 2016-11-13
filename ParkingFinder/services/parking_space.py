# -*- coding: utf-8 -*-
"""Parking Space Service.

This module contains all the service method related to parking space's information,
includes:
request parking space,
reserve parking space,
post parking space,
checkin parking space,
checkout parking space,

Flow:
    1. Request
    2. Reserve
    3. checkin
    4. post
    5. checkout

Todo:


"""

from clay import config
from sqlalchemy.orm.exc import NoResultFound
from tornado.gen import coroutine, Return

from ParkingFinder.base.errors import BaseError, NotFound
from ParkingFinder.base.with_repeat import with_repeat
from ParkingFinder.repositories import (
    AvailableParkingSpacePool,
    MatchedParkingList,
    ParkingLotRepository,
    WaitingPool,
)
from ParkingFinder.services.real_time_location_service import RealTimeLocationService

logger = config.get_logger('service.parking_space')


class ParkingSpaceService(object):

    @classmethod
    @with_repeat(repeat_exceptions=AwaitingMatching, timeout=300, duration=5)
    @coroutine
    def post_parking_space(cls, plate):
        """
        Publish a checked-in parking space to the Available Parking Space Pool
        Return a real time loc token with location of the other user if
        matching successfully, otherwise throw exception after timeout

        :param str plate: plate of the vehicle in the parking space
        :return RealTimeLocation: real time token with location of the matched waiting user
        :raises Timeout: timeout, user can send post request again to continue listening the status
        :raises AssertionError: the vehicle doesn't belong to the user with user_id
        :raises NotFound: the vehicle with given plate have not been checked in yet
        """

        try:
            parking_space = yield AvailableParkingSpacePool.read_one(plate=plate)
            if parking_space.is_active:
                raise AwaitingMatching

        except NoResultFound:
            try:
                parking_space = yield cls._post_new_parking_space(plate=plate)
                matched_parking = yield cls._matching_waiting_user(
                    posted_parking_space=parking_space
                )
                if not matched_parking:
                    raise AwaitingMatching
            except NoResultFound:
                raise NotFound

        real_time_location = yield cls._handle_matching_status(parking_space)
        raise Return(real_time_location)

    @classmethod
    @coroutine
    def _post_new_parking_space(cls, plate):
        """
        Mark a parking space in the parking lot as available and publish to the
        Available Parking Space Pool

        :param plate:
        :return AvailableParkingSpace:
        :raises AssertionError: The vehicle doesn't belong to the user with given user_id
        :raises NoResultFound: The vehicle with given plate have not been checked in yet
        """
        parking_space = yield ParkingLotRepository.read_one(plate=plate)

        available_parking_space = yield AvailableParkingSpacePool.insert(
            parking_space,
            is_active=False
        )
        raise Return(available_parking_space)

    @classmethod
    @with_repeat(repeat_exceptions=AwaitingAction, timeout=20, duration=1)
    @coroutine
    def _handle_matching_status(cls, parking_space):
        """
        This function will be self repeated every 1 seconds for 20 seconds
        if The user doesn't confirm with in 20 seconds, the handler function
        will throw a timeout exception. the caller should handle the release
        process in order to match next waiting user

        :param parking_space:
        :return RealTimeLocation: The user accept the parking space and the real time
            location service is established
        :raises Timeout: user is
        """
        try:
            matched_parking_space = (
                yield MatchedParkingList.read_one(plate=parking_space.plate)
            )
            if matched_parking_space.is_awaiting:
                # still waiting user's action
                raise AwaitingAction
            else:
                # The record should be removed no matter what decision user have made
                yield MatchedParkingList.remove(plate=matched_parking_space.plate)

                if matched_parking_space.is_reserved:
                    # user reserved the parking, the method will not remove itself from
                    # available parking space pool at this point because the waiting user
                    # might check in other parking space during the route
                    # the clean up step should be at checkout step
                    real_time_location = yield RealTimeLocationService.fetch_real_time_location(
                        plate=matched_parking_space
                    )
                    raise Return(real_time_location)

                if matched_parking_space.is_rejected:
                    # match parking with users in waiting pool
                    raise NoResultFound

        except NoResultFound:
            # this is happened because the waiting user has check into another parking spaces
            # on the way, match with another waiting user instead
            matched_parking_space = yield cls._matching_waiting_user(
                posted_parking_space=parking_space
            )
            if not matched_parking_space:
                raise AwaitingMatching
            else:
                raise AwaitingAction

    @classmethod
    @coroutine
    def _matching_waiting_user(cls, posted_parking_space):
        """
        Match a waiting user with given parking space, if the WaitingPool is empty,
        the parking space will mark as active in order to be matched when new
        waiting user is available

        :param AvailableParkingSpace posted_parking_space:
        :return MatchedParkingSpace: entity that holds both parking space and its matched user
        :return None: No waiting user found in the pool
        """
        waiting_user = yield WaitingPool.pop_one(
            longitude=posted_parking_space.longitude,
            latitude=posted_parking_space.latitude,
            location=posted_parking_space.location
        )
        if waiting_user:
            matching_record = cls._map_to_matched_parking(
                parking_space=posted_parking_space,
                waiting_user=waiting_user
            )
            pre_reserved_parking_space = yield MatchedParkingList.insert(
                matching_record=matching_record
            )
            raise Return(pre_reserved_parking_space)
        else:
            yield AvailableParkingSpacePool.update(
                plate=posted_parking_space.plate,
                is_active=True
            )
            raise Return(None)

    @staticmethod
    def _map_to_matched_parking(parking_space, waiting_user):
        """
        Map a parking space and a waiting user to matchedParking Entity

        :param AvailableParkingSpace parking_space:
        :param WaitingUser waiting_user:
        :return MatchedParkingSpace: The entity that contains both AvailableParkingSpace and WaitingUser
        """
        return False


class AwaitingAction(BaseError):
    pass


class AwaitingMatching(BaseError):
    pass


