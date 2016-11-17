import pytest
import datetime
from doubles import expect

from ParkingFinder.services import user_request as module
from ParkingFinder.entities import *
from ParkingFinder.services.user_request import NoResultFoundInMatchedSpaceTable


@pytest.mark.gen_test
# TODO: good
def test_request_parking_space_when_user_exist_in_matched_table_and_find_space():
    """
    test to check to see if can properly fetch result if every step is correct
    :return:
    """

    _user_id = 'DaPP'
    _waiting_user = WaitingUser.get_mock_object(overrides={'user_id': _user_id})
    _space_element = AvailableParkingSpace.get_mock_object()
    _space_return = [_space_element]
    expect(module.WaitingUserPool).read_one(user_id=_waiting_user.user_id).twice().and_return_future(_waiting_user)
    expect(module.UserRequestService)._loop_checking_space_availability(
        user_id=_waiting_user.user_id).and_return_future(_space_return)
    result = yield module.UserRequestService.request_parking_space(waiting_user=_waiting_user)
    assert result == _space_return


@pytest.mark.gen_test
# TODO: good
def test_request_parking_space_when_user_exist_in_matched_table_and_timeout():

    _user_id = 'DaPP'
    _waiting_user = WaitingUser.get_mock_object(overrides={'user_id': _user_id})
    expect(module.WaitingUserPool).read_one(user_id=_waiting_user.user_id).twice().and_return_future(_waiting_user)
    expect(module.UserRequestService)._loop_checking_space_availability(
        user_id=_waiting_user.user_id
    ).and_raise(module.Timeout)

    with pytest.raises(module.Timeout):
        yield module.UserRequestService.request_parking_space(waiting_user=_waiting_user)


# @pytest.mark.gen_test
# # TODO: bad
# def test_request_parking_space_when_user_does_not_exist_in_matched_table_and_timeout():
#
#     _user_id = 'DaPP'
#     _waiting_user = WaitingUser.get_mock_object(
#         overrides={
#             'user_id': _user_id
#         })
#     _waiting_user_second = WaitingUser.get_mock_object(
#         overrides={
#             'user_id': _user_id
#         })
#     expect(module.WaitingUserPool).read_one(
#         user_id=_waiting_user.user_id
#     ).and_raise(module.NoResultFound)
#
#     expect(module.WaitingUserPool).insert(
#         waiting_user=_waiting_user
#     ).and_return_future(_waiting_user)
#
#     expect(module.UserRequestService)._checking_space_availability(
#         waiting_user=_waiting_user
#     ).and_raise(module.Timeout)
#
#     expect(module.WaitingUserPool).read_one(
#         user_id=_waiting_user_second.user_id
#     ).and_return_future(_waiting_user_second)
#
#     with pytest.raises(module.Timeout):
#         yield module.UserRequestService.request_parking_space(waiting_user=_waiting_user)


@pytest.mark.gen_test
# TODO: good
def test_request_parking_space_when_user_does_not_exist_in_matched_table_and_does_not_exist_again():

    _user_id = 'DaPP'
    _waiting_user = WaitingUser.get_mock_object(overrides={'user_id': _user_id})
    expect(module.WaitingUserPool).read_one(user_id=_waiting_user.user_id).and_raise(module.NoResultFound)
    expect(module.WaitingUserPool).insert(waiting_user=_waiting_user).and_return_future(_waiting_user)
    expect(module.UserRequestService)._checking_space_availability(
        waiting_user=_waiting_user
    ).and_raise(module.Timeout)
    with pytest.raises(module.UserTerminatedInTheHalfWay):
        yield module.UserRequestService.request_parking_space(waiting_user=_waiting_user)


# @pytest.mark.gen_test
# # TODO: good
# def test_accept_parking_space_when_user_does_not_terminate_and_not_expired():
#     _user_id = 'DaPP'
#     _waiting_user = WaitingUser.get_mock_object(overrides={'user_id': _user_id})
#     _accept_plate = '1234567'
#     _accepted_space = MatchedParkingSpace.get_mock_object(overrides={'user_id': _user_id,
#                                                                      'plate': '1234567',
#                                                                      'status': 'awaiting'})
#     _rejected_space = MatchedParkingSpace.get_mock_object(overrides={'user_id': _user_id,
#                                                                      'plate': '7777333',
#                                                                      'status': 'awaiting'})
#
#     _real_time_location = RealTimeLocation.get_mock_object()
#     _list_of_space = [_accepted_space, _rejected_space]
#
#     expect(module.MatchedParkingList).read_many(
#         user_id=_user_id
#     ).and_return_future(_list_of_space)
#
#     expect(module.MatchedParkingList).update.and_return_future(1)
#
#     expect(module.WaitingUserPool).remove(user_id=_user_id).and_return_future(_waiting_user)
#     expect(module.RealTimeLocationService).fetch_real_time_location(
#         token=_accept_plate
#     ).and_return_future(_real_time_location)
#     result = yield module.UserRequestService.accept_parking_space(
#         user_id=_user_id,
#         accepted_space_plate=_accept_plate)
#     assert result == _real_time_location


@pytest.mark.gen_test
# TODO: good
def test_accept_parking_space_when_user_expired():
    _user_id = 'DaPP'
    _accept_plate = '1234567'
    _waiting_user = WaitingUser.get_mock_object(overrides={'user_id': _user_id})
    expect(module.MatchedParkingList).read_many(user_id=_user_id).and_raise(module.NoResultFound)
    with pytest.raises(module.Timeout):
        yield module.UserRequestService.accept_parking_space(user_id=_user_id,
                                                             accepted_space_plate=_accept_plate)


@pytest.mark.gen_test
# TODO: good
def test_accept_parking_space_when_user_terminate():
    _user_id = 'DaPP'
    _waiting_user = WaitingUser.get_mock_object(overrides={'user_id': _user_id})
    _accept_plate = '1234567'
    _accepted_space = MatchedParkingSpace.get_mock_object(
        overrides={
            'user_id': _user_id,
            'plate': '1234567',
            'status': 'awaiting'
        })
    _rejected_space = MatchedParkingSpace.get_mock_object(
        overrides={
            'user_id': _user_id,
            'plate': '7777333',
            'status': 'awaiting'
        })
    _list_of_space = [_accepted_space, _rejected_space]
    expect(module.MatchedParkingList).read_many(
        user_id=_user_id
    ).and_return_future(_list_of_space)

    expect(module.MatchedParkingList).update.and_return_future(1)

    expect(module.WaitingUserPool).remove(user_id=_user_id).and_return_future(None)
    expect(module.MatchedParkingList).update(
        user_id=_user_id,
        plate=_list_of_space[0].plate,
        status='rejected', ).and_return_future(1)
    with pytest.raises(module.UserTerminatedInTheHalfWay):
        yield module.UserRequestService.accept_parking_space(
            user_id=_user_id,
            accepted_space_plate=_accept_plate)

@pytest.mark.gen_test
# TODO:good
def test_reject_all_parking_when_use_does_not_terminate_not_timeout():
    _user_id = 'DaPP'
    _waiting_user = WaitingUser.get_mock_object(
        overrides={
            'user_id': _user_id
        })
    _accepted_space = MatchedParkingSpace.get_mock_object(
        overrides={'user_id': _user_id,
                   'plate': '1234567',
                   'status': 'awaiting'
                   })
    _rejected_space = MatchedParkingSpace.get_mock_object(
        overrides={'user_id': _user_id,
                   'plate': '7777333',
                   'status': 'awaiting'
                   })
    _final_space = AvailableParkingSpace.get_mock_object()
    _list_of_space = [_accepted_space, _rejected_space]
    _list_of_return_space= [_final_space]

    expect(module.MatchedParkingList).read_many(
        user_id=_waiting_user.user_id).and_return_future(_list_of_space)
    expect(module.MatchedParkingList).update(
        user_id=_user_id,
        plate=_list_of_space[0].plate,
        status='rejected', ).and_return_future(1)

    expect(module.MatchedParkingList).update(
        user_id=_user_id,
        plate=_list_of_space[1].plate,
        status='rejected', ).and_return_future(1)

    expect(module.UserRequestService)._checking_space_availability(
        waiting_user=_waiting_user
    ).and_return_future(_list_of_return_space)
    expect(module.WaitingUserPool).read_one(
        user_id=_waiting_user.user_id
    ).and_return_future(_waiting_user)

    result = yield module.UserRequestService.reject_all_parking(
        waiting_user=_waiting_user)
    assert result == _list_of_return_space


@pytest.mark.gen_test
# TODO:good
def test_reject_all_parking_when_use_does_not_terminate_time_out():
    _user_id = 'DaPP'
    _waiting_user = WaitingUser.get_mock_object(
        overrides={
            'user_id': _user_id
        })
    _accepted_space = MatchedParkingSpace.get_mock_object(
        overrides={'user_id': _user_id,
                   'plate': '1234567',
                   'status': 'awaiting'
                   })
    _rejected_space = MatchedParkingSpace.get_mock_object(
        overrides={'user_id': _user_id,
                   'plate': '7777333',
                   'status': 'awaiting'
                   })
    _final_space = AvailableParkingSpace.get_mock_object()
    _list_of_space = [_accepted_space, _rejected_space]

    expect(module.MatchedParkingList).read_many(
        user_id=_waiting_user.user_id).and_return_future(_list_of_space)
    expect(module.MatchedParkingList).update(
        user_id=_user_id,
        plate=_list_of_space[0].plate,
        status='rejected', ).and_return_future(1)

    expect(module.MatchedParkingList).update(
        user_id=_user_id,
        plate=_list_of_space[1].plate,
        status='rejected', ).and_return_future(1)

    expect(module.UserRequestService)._checking_space_availability(
        waiting_user=_waiting_user
    ).and_return_future(None)
    expect(module.WaitingUserPool).read_one(
        user_id=_waiting_user.user_id
    ).and_return_future(_waiting_user)

    with pytest.raises(module.Timeout):
        yield module.UserRequestService.reject_all_parking(
            waiting_user=_waiting_user)


@pytest.mark.gen_test
# TODO: good
def test_reject_all_parking_when_use_does_terminate():
    _user_id = 'DaPP'
    _waiting_user = WaitingUser.get_mock_object(
        overrides={
            'user_id': _user_id
        })
    _accepted_space = MatchedParkingSpace.get_mock_object(
        overrides={'user_id': _user_id,
                   'plate': '1234567',
                   'status': 'awaiting'
                   })
    _rejected_space = MatchedParkingSpace.get_mock_object(
        overrides={'user_id': _user_id,
                   'plate': '7777333',
                   'status': 'awaiting'
                   })
    _final_space = MatchedParkingSpace.get_mock_object(
        overrides={'user_id': _user_id,
                   'plate': '1231231',
                   'status': 'awaiting'
                   })

    _list_of_space = [_accepted_space, _rejected_space]
    _list_of_return_space = [_final_space]

    expect(module.MatchedParkingList).read_many(
        user_id=_waiting_user.user_id).and_return_future(_list_of_space)

    expect(module.MatchedParkingList).update(
        user_id=_user_id,
        plate=_list_of_space[0].plate,
        status='rejected', ).and_return_future(1)

    expect(module.MatchedParkingList).update(
        user_id=_user_id,
        plate=_list_of_space[1].plate,
        status='rejected', ).and_return_future(1)

    expect(module.UserRequestService)._checking_space_availability(
        waiting_user=_waiting_user
    ).and_return_future(_list_of_return_space)

    expect(module.WaitingUserPool).read_one(
        user_id=_waiting_user.user_id
    ).and_raise(module.NoResultFound)

    expect(module.MatchedParkingList).update(
        user_id=_user_id,
        plate=_list_of_return_space[0].plate,
        status='rejected',
    ).and_return_future(1)

    with pytest.raises(module.UserTerminatedInTheHalfWay):
        yield module.UserRequestService.reject_all_parking(
            waiting_user=_waiting_user)


@pytest.mark.gen_test
# TODO: good
def test_fetching_space_nearby_no_exception():
    _plate = '1234567'
    _available_space_1 = AvailableParkingSpace.get_mock_object(
        overrides={
            'plate': _plate
        })
    _available_space_2 = AvailableParkingSpace.get_mock_object(
        overrides={
            'plate': _plate
        })
    _available_space_3 = AvailableParkingSpace.get_mock_object(
        overrides={
            'plate': _plate
        })
    _list_of_available_space = [_available_space_1,
                                _available_space_2,
                                _available_space_3]
    expect(module.AvailableParkingSpacePool).read_many(
        latitude='12312312',
        longitude='12312321',
        location='DaPP').and_return_future(_list_of_available_space)
    result = yield module.UserRequestService.fetching_space_nearby(
        latitude='12312312',
        longitude='12312321',
        location='DaPP')
    assert result == _list_of_available_space


@pytest.mark.gen_test
# TODO: good
def test_fetching_space_nearby_with_exception():
    expect(module.AvailableParkingSpacePool).read_many(
        latitude='12312312',
        longitude='12312321',
        location='DaPP').and_raise(module.NoResultFound)
    with pytest.raises(module.NoResultFound):
        yield module.UserRequestService.fetching_space_nearby(
            latitude='12312312',
            longitude='12312321',
            location='DaPP')


@pytest.mark.gen_test
# TODO: good
def test_loop_checking_space_availability_with_timeout_and_space_not_suitable():
    _user_id = 'DaPP'
    _waiting_user = WaitingUser.get_mock_object(
        overrides={
            'user_id': _user_id
        })
    _accepted_space = MatchedParkingSpace.get_mock_object(
        overrides={'user_id': _user_id,
                   'plate': '1234567',
                   'status': 'rejected'
                   })
    _list_of_space = [_accepted_space]
    expect(module.MatchedParkingList).read_many(
        user_id=_user_id
    ).and_return_future(_list_of_space)
    with pytest.raises(module.Timeout):
        yield module.UserRequestService._loop_checking_space_availability(user_id=_user_id)


@pytest.mark.gen_test
# TODO: good
def test_loop_checking_space_availability_space_suitable():
    _user_id = 'DaPP'
    _plate ='1234567'
    _waiting_user = WaitingUser.get_mock_object(
        overrides={
            'user_id': _user_id
        })
    _accepted_space = MatchedParkingSpace.get_mock_object(
        overrides={'user_id': _user_id,
                   'plate': '1234567',
                   'status': 'awaiting'
                   })
    _list_of_space = [_accepted_space]

    _available_space = AvailableParkingSpace.get_mock_object(
        overrides={
            'plate': '1234567'
        }
    )
    _list_of_available = [_available_space]
    expect(module.MatchedParkingList).read_many(
        user_id=_user_id
    ).and_return_future(_list_of_space)

    expect(module.AvailableParkingSpacePool).read_one(
        plate=_plate
    ).and_return_future(_available_space)

    result = yield module.UserRequestService._loop_checking_space_availability(user_id=_user_id)
    assert result == _list_of_available


@pytest.mark.gen_test
#TODO: good
def test_checking_space_availability_with_find_in_no_loop():
    _user_id = 'DaPP'
    _waiting_user = WaitingUser.get_mock_object(
        overrides={
            'user_id': _user_id,
            'latitude': '12312312',
            'longitude': '12312321',
            'location': 'DaPP'
        })
    _available_space = AvailableParkingSpace.get_mock_object(
        overrides={
            'plate': '1234567',
            'latitude': '12312312',
            'longitude': '12312321',
            'location': 'DaPP'
        }
    )
    _list_of_available_space = [_available_space]
    _matched_space = MatchedParkingSpace.get_mock_object(
        overrides={
            'plate': '1234567',
            'user_id': _waiting_user.user_id,
            'status': 'awaiting'
        }
    )

    expect(module.AvailableParkingSpacePool).pop_many(
        latitude=_waiting_user.latitude,
        longitude=_waiting_user.longitude,
        location=_waiting_user.location
    ).and_return_future(_list_of_available_space)

    expect(module.MatchedParkingList).insert.and_return_future(_matched_space)

    result = yield module.UserRequestService._checking_space_availability(waiting_user=_waiting_user)
    assert result == _list_of_available_space


@pytest.mark.gen_test
def test_checking_space_availability_with_find_in_loop():
    _user_id = 'DaPP'
    _waiting_user = WaitingUser.get_mock_object(
        overrides={
            'user_id': _user_id,
            'latitude': '12312312',
            'longitude': '12312321',
            'location': 'DaPP'
        })
    _available_space = AvailableParkingSpace.get_mock_object(
        overrides={
            'plate': '1234567',
            'latitude': '12312312',
            'longitude': '12312321',
            'location': 'DaPP'
        }
    )
    _list_of_available_space = [_available_space]

    expect(module.AvailableParkingSpacePool).pop_many(
        latitude=_waiting_user.latitude,
        longitude=_waiting_user.longitude,
        location=_waiting_user.location
    ).and_raise(module.NoResultFound)

    expect(module.WaitingUserPool).update(
        user_id=_waiting_user.user_id,
        is_active=True
    ).and_return_future(1)

    expect(module.UserRequestService)._loop_checking_space_availability.and_return_future(_list_of_available_space)

    result = yield module.UserRequestService._checking_space_availability(waiting_user=_waiting_user)
    assert _list_of_available_space == result


@pytest.mark.gen_test
def test_service_terminate_successfully():
    _user_id='DaPP'
    expect(module.WaitingUserPool).remove(user_id=_user_id).and_return_future(None)
    with pytest.raises(module.CanNotStopForwardingMessage):
        yield module.UserRequestService.service_terminate(user_id=_user_id)


