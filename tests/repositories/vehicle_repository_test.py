import pytest

from doubles import expect
from schematics.exceptions import ValidationError
from sqlalchemy.orm.exc import NoResultFound

from ParkingFinder.entities.vehicle import Vehicle
from ParkingFinder.entities.user import User
from ParkingFinder.repositories.user_repository import UserRepository
from ParkingFinder.repositories import vehicle_repository as module


# retrieve such a car in the database
# 'plate': '6ELA725',
# 'brand': 'Toyota',
# 'model': 'Matrix',
# 'color': 'Golden',
# 'year': 2009,

@pytest.mark.gen_test
def test_retrieve_vehicle_by_plate():
    vehicle = yield module.VehicleRepository.retrieve_vehicle_by_plate(plate='6ELA725')
    vehicle.validate()
    assert vehicle.plate == '6ELA725'
    assert vehicle.brand == 'Toyota'
    assert vehicle.model == 'Matrix'
    assert vehicle.color == 'Golden'
    assert vehicle.year == 2009


@pytest.mark.gen_test
def test_insert_vehicle():
    mocked_vehicle = Vehicle.get_mock_object()
    vehicle = yield module.VehicleRepository._insert_vehicle(vehicle=mocked_vehicle)
    _vehicle = yield module.VehicleRepository.retrieve_vehicle_by_plate(plate=mocked_vehicle.plate)
    assert _vehicle == vehicle


# 'user_id': 'valid_account_2',
#         'plate': 'ANRCHST',
# 'user_id': 'valid_account_2',
#         'plate': '4JTY881',
@pytest.mark.gen_test
def test_retrieve_vehicle_by_user():
    vehicles = yield module.VehicleRepository.retrieve_vehicle_by_user(user_id='valid_account_2')
    _vehicle1 = yield module.VehicleRepository.retrieve_vehicle_by_plate(plate='ANRCHST')
    _vehicle2 = yield module.VehicleRepository.retrieve_vehicle_by_plate(plate='4JTY881')
    assert len(vehicles) == 2
    if vehicles[0] == _vehicle1 and vehicles[1] == _vehicle2:
        assert 1 == 1
    elif vehicles[0] == _vehicle2 and vehicles[1] == _vehicle1:
        assert 1 == 1
    else:
        assert 1 == 0


@pytest.mark.gen_test
def test_insert_registered_vehicle():
    mocked_user = User.get_mock_object()
    mocked_vehicle = Vehicle.get_mock_object()
    user = yield UserRepository.upsert(mocked_user)
    vehicle = yield module.VehicleRepository.insert_registered_vehicle(user_id=user.user_id,
                                                                       vehicle=mocked_vehicle)
    _vehicle = yield module.VehicleRepository.retrieve_vehicle_by_plate(plate=mocked_vehicle.plate)
    assert vehicle == _vehicle



