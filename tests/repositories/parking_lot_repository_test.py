import pytest

from doubles import expect
from datetime import datetime
from schematics.exceptions import ValidationError
from sqlalchemy.orm.exc import NoResultFound

from ParkingFinder.entities.parking_space import ParkingSpace
from ParkingFinder.entities.parking_space import Location
from ParkingFinder.repositories import parking_lot as module


@pytest.mark.gen_test
def test_read_one_with_result():
    parking_space = yield module.ParkingLotRepository.read_one(plate='6ELA540')
    parking_space.validate()
    assert parking_space.plate == '6ELA540'
    assert parking_space.location.latitude == 34.061386
    assert parking_space.location.longitude == -118.433819
    assert parking_space.location.location == 'UCLA'
    assert parking_space.created_at == datetime(2016, 11, 15, 10, 12, 5)
    assert parking_space.location.level == 1


@pytest.mark.gen_test
def test_read_one_with_no_result():
    expect(module.ParkingSpaceMapper).to_entity.never()
    with pytest.raises(NoResultFound):
        yield module.ParkingLotRepository.read_one(plate='TML1234')


@pytest.mark.gen_test
def test_insert():
    mock_location = Location.get_mock_object(overrides={
        'latitude': 15.6789,
        'longitude': 56.1234,
    })
    del mock_location['location'], mock_location['level']
    mock_parking_space = ParkingSpace.get_mock_object(overrides={
        'plate': '6DAY434',
        'location': mock_location,
    })
    parking_space = yield module.ParkingLotRepository.insert(mock_parking_space)
    _parking_space = yield module.ParkingLotRepository.read_one('6DAY434')
    del parking_space['created_at'], _parking_space['created_at']
    assert parking_space == _parking_space


@pytest.mark.gen_test
def test_remove():
    num = yield module.ParkingLotRepository.remove('6DAY434')
    assert num == 1
    expect(module.ParkingSpaceMapper).to_entity.never()
    with pytest.raises(NoResultFound):
        yield module.ParkingLotRepository.read_one(plate='6DAY434')

