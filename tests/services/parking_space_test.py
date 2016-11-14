import pytest
from doubles import expect

from ParkingFinder.services import parking_space as module
from ParkingFinder.entities import *


@pytest.mark.gen_test
def test_post_parking_space_with_active_available_parking():
    _plate = "1234567"
    _parking_space = ParkingSpace.get_mock_object(overrides={'plate': _plate})
    _posted_parking_space = PostedParkingSpace.get_mock_object(
        overrides={'parking_space': _parking_space, 'is_active': True}
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
    _posted_parking_space = PostedParkingSpace.get_mock_object(
        overrides={'parking_space': _parking_space, 'is_active': False}
    )
    expect(module.AvailableParkingSpacePool).read_one(plate=_plate).and_return_future(_posted_parking_space)

    expect(module.AvailableParkingSpacePool)._handle_matching_status(
        parking_space=_posted_parking_space
    ).twice().and_raise(module.Timeout)

    with pytest.raises(module.Timeout):
        yield module.ParkingSpaceService.post_parking_space(plate=_plate)


def test_post_parking_space_with_untrustworthy_waiting_user():
    """
    The user check-in the a parking space other than the one he reserved.
    The checkin process should remove the matched_parking_space from the db, and the parking space
    will match a new waiting user.
    """
    _plate = "1234567"
    _parking_space = ParkingSpace.get_mock_object(overrides={'plate': _plate})
    _posted_parking_space = PostedParkingSpace.get_mock_object(
        overrides={'parking_space': _parking_space, 'is_active': False}
    )
    expect(module.AvailableParkingSpacePool).read_one(
        plate=_plate
    ).twice().and_return_future(_posted_parking_space)

    expect(module.AvailableParkingSpacePool)._handle_matching_status(
        parking_space=_posted_parking_space
    ).twice().and_raise(module.AwaitingMatching)

    with pytest.raises(module.Timeout):
        yield module.ParkingSpaceService.post_parking_space(plate=_plate)


@pytest.mark.gen_test
def test_post_parking_space_with_post_new_parking_space():
    pass


@pytest.mark.gen_test
def test_post_parking_space_with_posting_invalid_plate():
    pass


@pytest.mark.gen_test
def test_post_parking_space_with_matched_waiting_user():
    pass


@pytest.mark.gen_test
def test_post_parking_space_with_no_withing_user():
    pass
