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
from tornado.gen import coroutine, Return, sleep

from ParkingFinder.base.errors import BaseError, NotFound, Timeout
from ParkingFinder.base.with_repeat import with_repeat
from ParkingFinder.entities.matched_parking_space import MatchedParkingSpace
from ParkingFinder.entities.available_parking_space import AvailableParkingSpace
from ParkingFinder.repositories import (
    AvailableParkingSpacePool,
    MatchedParkingList,
    ParkingLotRepository,
    WaitingUserPool,
)
from ParkingFinder.services.real_time_location_service import RealTimeLocationService

logger = config.get_logger('service.parking_space')

awaiting_matching_time_out = config.get('matching.matching_timeout')
awaiting_matching_duration = config.get('matching.matching_duration')
awaiting_matching_repeat_times = config.get('matching.matching_repeat_times')
awaiting_action_time_out = config.get('matching.awaiting_action_timeout')
awaiting_action_duration = config.get('matching.awaiting_action_duration')
awaiting_action_repeat_times = config.get('matching.awaiting_action_repeat_times')


class AwaitingAction(BaseError):
    error = "Awaiting Action"


class AwaitingMatching(BaseError):
    error = 'Awaiting Matching'


class ParkingSpaceService(object):

    @classmethod
    @with_repeat(
        repeat_exceptions=AwaitingMatching,
        repeat_times=awaiting_matching_repeat_times,
        timeout=awaiting_matching_time_out,
        duration=awaiting_matching_duration,
    )
    @coroutine
    def post_parking_space(cls, plate):
        """
        Publish a checked-in parking space to the Available Parking Space Pool
        Return a real time loc token with location of the other user if
        matching successfully, otherwise throw exception after timeout
        :param str plate: plate of the vehicle in the parking space
        :return parking_space: parking_space
        :raises Timeout: timeout, user can send post request again to continue listening the status
        :raises NotFound: the vehicle with given plate have not been checked in yet
        """

        try:
            parking_space = yield AvailableParkingSpacePool.read_one(plate=plate)
            if parking_space.is_active:
                raise AwaitingMatching

        except NoResultFound:
            try:
                parking_space = yield cls._post_new_parking_space(plate=plate)
            except NoResultFound:
                raise NotFound

        try:
            vehicle = yield cls._handle_matching_status(
                parking_space=parking_space
            )
            raise Return(vehicle)
        except Timeout:
            # simply ignore timeout exception of _handle_matching_status and get into
            # next round, the _handle_matching_status will remove the entry if
            # expired and matches a new waiting user
            raise AwaitingMatching

    @classmethod
    @coroutine
    def _post_new_parking_space(cls, plate):
        """
        Mark a parking space in the parking lot as available and publish to the
        Available Parking Space Pool

        :param plate:
        :return AvailableParkingSpace:
        :raises NoResultFound: The vehicle with given plate have not been checked in yet
        """
        parking_space = yield ParkingLotRepository.read_one(plate=plate)
        location = {
            'longitude': parking_space.location.longitude,
            'latitude': parking_space.location.latitude,
        }
        if parking_space.location.level:
            location.update({'level': parking_space.location.level})
        if parking_space.location.location:
            location.update({'location': parking_space.location.location})

        available_parking_space = yield AvailableParkingSpacePool.insert(
            available_parking_space=AvailableParkingSpace({
                'plate': parking_space.plate,
                'location': location,
                'is_active': False
            })
        )
        raise Return(available_parking_space)

    @classmethod
    @with_repeat(
        repeat_exceptions=AwaitingAction,
        timeout=awaiting_action_time_out,
        repeat_times=awaiting_action_repeat_times,
        duration=awaiting_action_duration,
    )
    @coroutine
    def _handle_matching_status(cls, parking_space):
        """
        This function will be self repeated every 1 seconds for 20 seconds
        if The user doesn't confirm with in 20 seconds, the handler function
        will throw a timeout exception. the caller should handle the release
        process in order to match next waiting user

        :param parking_space:
        :return Vehicle: The user accept the parking space
        :raises Timeout: user is
        :raises AwaitingMatching: No available user in the pool
        """
        try:
            matched_parking_space = (
                yield MatchedParkingList.read_one(plate=parking_space.plate)
            )

            # if expired, wait for a second to avoid race condition.
            if matched_parking_space.is_time_expired:
                yield sleep(1)
                matched_parking_space = (
                    yield MatchedParkingList.read_one(plate=parking_space.plate)
                )

            # if the race condition is occurred, the other side mark
            # the matched record as reserved after time expired, it will
            # be seen as a valid reservation.
            if matched_parking_space.is_reserved:
                # The record should be removed no matter what decision user have made
                yield MatchedParkingList.remove(plate=matched_parking_space.plate)
                # user reserved the parking, the method will not remove itself from
                # available parking space pool at this point because the waiting user
                # might check in other parking space during the route
                # the clean up step should be at checkout step
                vehicle = yield ParkingLotRepository.read_one(plate=parking_space.plate)
                raise Return(vehicle)

            elif matched_parking_space.is_awaiting:
                # still waiting user's action
                raise AwaitingAction
            elif matched_parking_space.is_expired or matched_parking_space.is_rejected:
                yield MatchedParkingList.remove(plate=parking_space.plate)
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
        Match a waiting user with given parking space, if the WaitingUserPool is empty,
        the parking space will mark as active in order to be matched when new
        waiting user is available

        :param AvailableParkingSpace posted_parking_space:
        :return MatchedParkingSpace: entity that holds both parking space and its matched user
        :return None: No waiting user found in the pool
        """
        waiting_user = yield WaitingUserPool.pop_one(
            longitude=posted_parking_space.location.longitude,
            latitude=posted_parking_space.location.latitude,
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
        return MatchedParkingSpace({
            'parking_space': parking_space.plate,
            'waiting_user': waiting_user.user_id,
        })
