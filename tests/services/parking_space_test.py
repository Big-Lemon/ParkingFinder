import pytest
import datetime
from doubles import expect

from ParkingFinder.services import parking_space as module
from ParkingFinder.entities import *


@pytest.mark.gen_test
def test_post_parking_space_with_active_available_parking():
    _plate = "1234567"
    _parking_space = ParkingSpace.get_mock_object(overrides={'plate': _plate})
    _posted_parking_space = AvailableParkingSpace.get_mock_object(
        overrides={'plate': _plate, 'is_active': True}
    )
    expect(module.AvailableParkingSpacePool).read_one(plate=_plate).and_return_future(_posted_parking_space)

    with pytest.raises(module.Timeout):
        yield module.ParkingSpaceService.post_parking_space(plate=_plate)


@pytest.mark.gen_test
def test_post_parking_space_with_matching_timeout():
    """
    the parking space is matched with a waiting user, however, the user didn't confirm
    the reservation with in certain times(15 secs), therefore, the _handle_matching_status throws
    Timeout exception, after matching times(300 secs)
    """
    _plate = "1234567"
    _parking_space = ParkingSpace.get_mock_object(overrides={'plate': _plate})
    _posted_parking_space = AvailableParkingSpace.get_mock_object(
        overrides={'plate': _plate, 'is_active': False}
    )
    expect(module.AvailableParkingSpacePool).read_one(plate=_plate).and_return_future(_posted_parking_space)

    expect(module.ParkingSpaceService)._handle_matching_status(
        parking_space=_posted_parking_space
    ).twice().and_raise(module.Timeout)

    with pytest.raises(module.Timeout):
        yield module.ParkingSpaceService.post_parking_space(plate=_plate)


@pytest.mark.gen_test
def test_post_parking_space_with_untrustworthy_waiting_user():
    """
    The user check-in the a parking space other than the one he reserved.
    The checkin process should remove the matched_parking_space from the db, and the parking space
    will match a new waiting user.
    """
    _plate = "1234567"
    _parking_space = ParkingSpace.get_mock_object(overrides={'plate': _plate})
    _posted_parking_space = AvailableParkingSpace.get_mock_object(
        overrides={'plate': _plate, 'is_active': False}
    )

    expect(module.AvailableParkingSpacePool).read_one(
        plate=_plate
    ).twice().and_return_future(_posted_parking_space)

    expect(module.ParkingSpaceService)._handle_matching_status(
        parking_space=_posted_parking_space
    ).and_raise(module.AwaitingMatching)

    with pytest.raises(module.Timeout):
        yield module.ParkingSpaceService.post_parking_space(plate=_plate)


@pytest.mark.gen_test
def test_post_parking_space_with_post_new_parking_space():
    """
    """
    _plate = "1234567"
    _parking_space = ParkingSpace.get_mock_object(overrides={'plate': _plate})
    _posted_parking_space = AvailableParkingSpace.get_mock_object(
        overrides={'plate': _plate, 'is_active': False}
    )
    _real_time_location = RealTimeLocation.get_mock_object()

    # The parking space has not been posted yet
    expect(module.AvailableParkingSpacePool).read_one(
        plate=_plate
    ).once().and_raise(module.NoResultFound)

    expect(module.ParkingSpaceService)._post_new_parking_space(
        plate=_plate
    ).once().and_return_future(_posted_parking_space)

    expect(module.ParkingSpaceService)._handle_matching_status(
        parking_space=_posted_parking_space
    ).once().and_return_future(_real_time_location)

    result = yield module.ParkingSpaceService.post_parking_space(plate=_plate)
    assert _real_time_location == result


@pytest.mark.gen_test
def test_post_parking_space_with_posting_invalid_plate():
    """
    """
    _plate = "1234567"
    _parking_space = ParkingSpace.get_mock_object(overrides={'plate': _plate})
    _posted_parking_space = AvailableParkingSpace.get_mock_object(
        overrides={'plate': _plate, 'is_active': False}
    )
    _real_time_location = RealTimeLocation.get_mock_object()

    # The parking space has not been posted yet
    expect(module.AvailableParkingSpacePool).read_one(
        plate=_plate
    ).and_raise(module.NoResultFound)

    expect(module.ParkingSpaceService)._post_new_parking_space(
        plate=_plate
    ).and_raise(module.NoResultFound)

    expect(module.ParkingSpaceService)._handle_matching_status.never()

    with pytest.raises(module.NotFound):
        yield module.ParkingSpaceService.post_parking_space(plate=_plate)


@pytest.mark.gen_test
def test_post_new_parking_space():
    """
    Successfully post a new parking space

    :return:
    """
    _plate = "1234567"
    _parking_space = ParkingSpace.get_mock_object(
        overrides={
            'plate': _plate
        })
    _available_parking_space = AvailableParkingSpace.get_mock_object({
        'plate': _plate,
        'is_active': False
    })
    expect(module.ParkingLotRepository).read_one(
        plate=_plate
    ).and_return_future(_parking_space)

    expect(module.AvailableParkingSpacePool).insert.and_return_future(_available_parking_space)

    result = yield module.ParkingSpaceService._post_new_parking_space(
        plate=_plate
    )
    assert result == _available_parking_space


@pytest.mark.gen_test
def test_post_new_parking_space():
    """
    Successfully post a new parking space

    :return:
    """
    _plate = "1234567"
    _parking_space = ParkingSpace.get_mock_object(
        overrides={
            'plate': _plate
        })
    _available_parking_space = AvailableParkingSpace.get_mock_object({
        'plate': _plate,
        'is_active': False
    })
    expect(module.ParkingLotRepository).read_one(
        plate=_plate
    ).and_return_future(_parking_space)

    expect(module.AvailableParkingSpacePool).insert.and_return_future(_available_parking_space)

    result = yield module.ParkingSpaceService._post_new_parking_space(
        plate=_plate
    )
    assert result == _available_parking_space


@pytest.mark.gen_test
def test_post_new_parking_space_with_not_found_in_parking_lot():
    """
    Successfully post a new parking space

    :return:
    """
    _plate = "1234567"
    _parking_space = ParkingSpace.get_mock_object(
        overrides={
            'plate': _plate
        })
    _available_parking_space = AvailableParkingSpace.get_mock_object({
        'plate': _plate,
        'is_active': False
    })
    expect(module.ParkingLotRepository).read_one(
        plate=_plate
    ).and_raise(module.NoResultFound)

    with pytest.raises(module.NoResultFound):
        yield module.ParkingSpaceService._post_new_parking_space(
            plate=_plate
        )


@pytest.mark.gen_test
def test_handle_matching_status_with_no_record_and_no_waiting_user():
    """
    :return:
    """
    _plate = '1234567'
    _parking_space = ParkingSpace.get_mock_object(overrides={
        'plate': _plate
    })
    expect(module.MatchedParkingList).read_one(
        plate=_plate
    ).and_raise(module.NoResultFound)

    expect(module.ParkingSpaceService)._matching_waiting_user.once(
    ).and_return_future(None)
    with pytest.raises(module.AwaitingMatching):
        yield module.ParkingSpaceService._handle_matching_status(
            parking_space=_parking_space
        )


@pytest.mark.gen_test
def test_handle_matching_status_with_no_record_and_waiting_user():
    _plate = '1234567'
    _parking_space = ParkingSpace.get_mock_object(overrides={
        'plate': _plate
    })
    _matched_parking_space = MatchedParkingSpace.get_mock_object(overrides={
        'plate': _plate
    })
    expect(module.MatchedParkingList).read_one(
        plate=_plate
    ).and_raise(module.NoResultFound)

    expect(module.ParkingSpaceService)._matching_waiting_user.twice(
    ).and_return_future(_matched_parking_space)

    with pytest.raises(module.Timeout):
        yield module.ParkingSpaceService._handle_matching_status(
            parking_space=_parking_space
        )


@pytest.mark.gen_test
def test_handle_matching_status_with_time_expired():
    _plate = '1234567'
    _parking_space = ParkingSpace.get_mock_object(overrides={
        'plate': _plate
    })
    _matched_parking_space = MatchedParkingSpace.get_mock_object(overrides={
        'plate': _plate,
        'status': 'expired',
        'created_at': datetime.datetime.utcnow() - datetime.timedelta(10)
    })

    expect(module.MatchedParkingList).read_one(
        plate=_plate
    ).and_return_future(_matched_parking_space)


    expect(module).sleep(1).twice().and_return_future(None)

    expect(module.MatchedParkingList).remove(
        plate=_matched_parking_space.plate
    ).twice().and_return_future(None)

    expect(module.ParkingSpaceService)._matching_waiting_user(
        posted_parking_space=_parking_space
    ).and_return_future(_matched_parking_space)

    with pytest.raises(module.Timeout):
        yield module.ParkingSpaceService._handle_matching_status(
            parking_space=_parking_space
        )

@pytest.mark.gen_test
def test_handle_matching_status_with_time_expired_and_race_condition():
    _plate = '1234567'
    _parking_space = ParkingSpace.get_mock_object(overrides={
        'plate': _plate
    })
    _matched_parking_space = MatchedParkingSpace.get_mock_object(overrides={
        'plate': _plate
    })

    expect(module.MatchedParkingList).read_one(
        plate=_plate
    ).and_return_future(_matched_parking_space)
    expect(module.MatchedParkingSpace).is_time_expired.and_return(True)
    expect(module.MatchedParkingSpace).is_reserved.and_return(True)

    expect(module).sleep(1).once().and_return_future(None)

    expect(module.MatchedParkingList).remove(
        plate=_matched_parking_space.plate
    ).once().and_return_future(None)

    expect(module.ParkingLotRepository).read_one(
        plate=_matched_parking_space.plate
    ).and_return_future(_parking_space)

    _result = yield module.ParkingSpaceService._handle_matching_status(
        parking_space=_parking_space
    )

    assert _result == _parking_space


@pytest.mark.gen_test
def test_handle_matching_status_with_awaiting_status():
    _plate = '1234567'
    _parking_space = ParkingSpace.get_mock_object(overrides={
        'plate': _plate
    })
    _matched_parking_space = MatchedParkingSpace.get_mock_object(overrides={
        'plate': _plate,
        'status': 'awaiting',
        'created_at': datetime.datetime.utcnow()
    })

    expect(module.MatchedParkingList).read_one(
        plate=_plate
    ).twice().and_return_future(_matched_parking_space)

    expect(module).sleep(1).never()

    expect(module.ParkingSpaceService)._matching_waiting_user.never()

    with pytest.raises(module.Timeout):
        yield module.ParkingSpaceService._handle_matching_status(
            parking_space=_parking_space
        )


@pytest.mark.gen_test
def test_handle_matching_status_with_rejected_status():
    _plate = '1234567'
    _parking_space = ParkingSpace.get_mock_object(overrides={
        'plate': _plate
    })
    _matched_parking_space = MatchedParkingSpace.get_mock_object(overrides={
        'plate': _plate,
        'status': 'rejected',
        'created_at': datetime.datetime.utcnow()
    })

    expect(module.MatchedParkingList).read_one(
        plate=_plate
    ).and_return_future(_matched_parking_space)

    expect(module).sleep(1).never()

    expect(module.MatchedParkingList).remove(
        plate=_matched_parking_space.plate
    ).once().and_return_future(None)

    expect(module.ParkingSpaceService)._matching_waiting_user(
        posted_parking_space=_parking_space
    ).and_return_future(None)

    with pytest.raises(module.AwaitingMatching):
        yield module.ParkingSpaceService._handle_matching_status(
            parking_space=_parking_space
        )
