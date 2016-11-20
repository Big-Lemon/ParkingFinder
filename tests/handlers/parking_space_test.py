import httplib
import json
import pytest
from doubles import expect

from ParkingFinder.handlers import parking_space as module
from ParkingFinder.handlers.app import app as application
from ParkingFinder.entities.access_token import AccessToken
from ParkingFinder.entities.parking_space import ParkingSpace
from ParkingFinder.entities.user import User
from ParkingFinder.entities.vehicle import Vehicle
from ParkingFinder.entities.available_parking_space import AvailableParkingSpace
from ParkingFinder.repositories.access_token_repository import AccessTokenRepository
from tornado.httpclient import HTTPError


@pytest.fixture
def app():
    return application


@pytest.fixture
def access_token():
    return AccessToken.get_mock_object(overrides={
        'user_id': '000000',
        'access_token': '111111'
    })


@pytest.mark.gen_test
def test_post_parking_space(http_client, base_url, access_token):
    url = base_url + '/parkingSpace/post/' + access_token.user_id

    plate = "1234567"
    parking_space = ParkingSpace.get_mock_object(
        overrides={
            "plate": plate
        }
    )
    expect(AccessTokenRepository).read_one(
        access_token=access_token.access_token
    ).and_return_future(
        access_token
    )

    """ --------test---------"""
    expect(module)._verify_vehicle_belonging(
        user_id=access_token.user_id,
        plate=plate
    ).and_return_future(True)

    expect(module.ParkingSpaceService).post_parking_space(
        plate=plate
    ).and_return_future(parking_space)

    response = yield http_client.fetch(
        url,
        method="PUT",
        body=json.dumps({
            "plate": plate,
            "access_token": access_token.access_token
        })
    )
    body = response.body
    _body = json.loads(body)
    _parking_space = _body.get('parking_space', None)

    assert _parking_space
    assert response.code == 200
    assert parking_space.plate == _parking_space['plate']
    assert parking_space.location.longitude == _parking_space['longitude']
    assert parking_space.location.latitude == _parking_space['latitude']
    assert parking_space.location.location == _parking_space.get('address')
    assert parking_space.location.level == _parking_space.get('level')


@pytest.mark.gen_test
def test_post_parking_space_with_no_matching_user(http_client, base_url, access_token):
    url = base_url + '/parkingSpace/post/' + access_token.user_id

    plate = "1234567"
    expect(AccessTokenRepository).read_one(
        access_token=access_token.access_token
    ).and_return_future(
        access_token
    )

    """ --------test---------"""
    expect(module)._verify_vehicle_belonging(
        user_id=access_token.user_id,
        plate=plate
    ).and_return_future(True)

    expect(module.ParkingSpaceService).post_parking_space(
        plate=plate
    ).and_raise(module.Timeout)

    response = yield http_client.fetch(
        url,
        method="PUT",
        body=json.dumps({
            "plate": plate,
            "access_token": access_token.access_token
        })
    )
    body = response.body
    _body = json.loads(body)
    _parking_space = _body.get('parking_space')

    assert not _parking_space
    assert response.code == 200


@pytest.mark.gen_test
def test_post_parking_space_with_non_checked_in_vehicle(http_client, base_url, access_token):
    url = base_url + '/parkingSpace/post/' + access_token.user_id

    plate = "1234567"
    expect(AccessTokenRepository).read_one(
        access_token=access_token.access_token
    ).and_return_future(
        access_token
    )

    """ --------test---------"""
    expect(module)._verify_vehicle_belonging(
        user_id=access_token.user_id,
        plate=plate
    ).and_return_future(True)

    expect(module.ParkingSpaceService).post_parking_space(
        plate=plate
    ).and_raise(module.NotFound)

    try:
        yield http_client.fetch(
            url,
            method="PUT",
            body=json.dumps({
                "plate": plate,
                "access_token": access_token.access_token
            })
        )
    except HTTPError as ex:
        assert ex.code == httplib.NOT_FOUND


@pytest.mark.gen_test
def test_reserve_parking_space(http_client, base_url, access_token):
    url = base_url + '/parkingSpace/reserve/' + access_token.user_id

    plate = "1234567"
    parking_space = ParkingSpace.get_mock_object(overrides={'plate': plate})
    vehicle = Vehicle.get_mock_object(overrides={'plate': plate})
    expect(AccessTokenRepository).read_one(
        access_token=access_token.access_token
    ).and_return_future(
        access_token
    )
    expect(module.UserRequestService).accept_parking_space(
        user_id=access_token.user_id,
        accepted_space_plate=plate,
    ).and_return_future(parking_space)
    expect(module.VehicleRepository).retrieve_vehicle_by_plate(
        plate=plate
    ).and_return_future(vehicle)

    response = yield http_client.fetch(
        url,
        method="POST",
        body=json.dumps({
            "plate": plate,
            "access_token": access_token.access_token
        })
    )

    body = json.loads(response.body)
    _parking_space = body.get('parking_space')
    _vehicle = body.get('vehicle')
    assert _parking_space and _vehicle
    assert _parking_space['plate'] == parking_space.plate
    assert _parking_space['latitude'] == parking_space.location.latitude
    assert _parking_space['longitude'] == parking_space.location.longitude
    assert _parking_space.get('level') == parking_space.location.level
    assert _parking_space.get('address') == parking_space.location.location

    assert _vehicle['plate'] == vehicle.plate
    assert _vehicle['model'] == vehicle.model
    assert _vehicle['brand'] == vehicle.brand
    assert _vehicle['color'] == vehicle.color
    assert _vehicle['year'] == vehicle.year


@pytest.mark.gen_test
def test_reserve_parking_space_with_expired_request(http_client, base_url, access_token):
    url = base_url + '/parkingSpace/reserve/' + access_token.user_id

    plate = "1234567"
    expect(AccessTokenRepository).read_one(
        access_token=access_token.access_token
    ).and_return_future(
        access_token
    )
    expect(module.UserRequestService).accept_parking_space(
        user_id=access_token.user_id,
        accepted_space_plate=plate,
    ).and_raise(module.Timeout)
    try:
        yield http_client.fetch(
            url,
            method="POST",
            body=json.dumps({
                "plate": plate,
                "access_token": access_token.access_token
            })
        )
    except HTTPError as ex:
        assert ex.code == httplib.REQUEST_TIMEOUT


@pytest.mark.gen_test
def test_reject_all(http_client, base_url, access_token):
    url = base_url + '/parkingSpace/reject/' + access_token.user_id
    available_parking_spaces = [AvailableParkingSpace.get_mock_object() for _ in range(3)]

    plate = "1234567"
    expect(AccessTokenRepository).read_one(
        access_token=access_token.access_token
    ).and_return_future(
        access_token
    )
    expect(module.UserRequestService).reject_all_parking(
        user_id=access_token.user_id,
    ).and_return_future(available_parking_spaces)

    response = yield http_client.fetch(
        url,
        method="POST",
        body=json.dumps({
            "plate": plate,
            "access_token": access_token.access_token
        })
    )
    body = json.loads(response.body)
    _available_parking_spaces = body['available_parking_spaces']
    assert _available_parking_spaces
    assert len(_available_parking_spaces) == len(available_parking_spaces)
    for i in range(3):
        _json = _available_parking_spaces[i]
        entity = available_parking_spaces[i]
        assert _json['plate'] == entity.plate
        assert _json['longitude'] == entity.location.longitude
        assert _json['latitude'] == entity.location.latitude
        assert _json.get('address') == entity.location.location
        assert _json.get('level') == entity.location.level


@pytest.mark.gen_test
def test_reject_all_with_no_available_parking_space(http_client, base_url, access_token):
    url = base_url + '/parkingSpace/reject/' + access_token.user_id

    plate = "1234567"
    expect(AccessTokenRepository).read_one(
        access_token=access_token.access_token
    ).and_return_future(
        access_token
    )
    expect(module.UserRequestService).reject_all_parking(
        user_id=access_token.user_id,
    ).and_raise(module.Timeout)

    try:
        yield http_client.fetch(
            url,
            method="POST",
            body=json.dumps({
                "plate": plate,
                "access_token": access_token.access_token
            })
        )
    except HTTPError as ex:
        assert ex.code == httplib.REQUEST_TIMEOUT


@pytest.mark.gen_test
def test_check_out(http_client, base_url, access_token):
    url = base_url + '/parkingSpace/checkout/' + access_token.user_id

    plate = "1234567"
    parking_space = ParkingSpace.get_mock_object(overrides={'plate': plate})
    expect(AccessTokenRepository).read_one(
        access_token=access_token.access_token
    ).and_return_future(
        access_token
    )
    expect(module)._verify_vehicle_belonging(
        user_id=access_token.user_id,
        plate=plate
    ).and_return_future(True)
    expect(module.ParkingLotRepository).remove(
        plate=plate
    ).and_return_future(parking_space)

    response = yield http_client.fetch(
        url,
        method="POST",
        body=json.dumps({
            "access_token": access_token.access_token,
            "plate": plate
        })
    )

    assert response.code == 200


@pytest.mark.gen_test
def test_check_in(http_client, base_url, access_token):
    url = base_url + '/parkingSpace/checkin/' + access_token.user_id

    plate = "1234567"
    longitude = 123.123
    latitude = 321.321

    parking_space = ParkingSpace.get_mock_object(
        overrides={
            'plate': plate,
            'location': {
                'latitude': latitude,
                'longitude': longitude
            }
        })
    expect(AccessTokenRepository).read_one(
        access_token=access_token.access_token
    ).and_return_future(
        access_token
    )
    expect(module)._verify_vehicle_belonging(
        user_id=access_token.user_id,
        plate=plate
    ).and_return_future(True)
    expect(module.ParkingLotRepository).insert.and_return_future(parking_space)
    expect(module.UserRequestService).service_terminate(
        user_id=access_token.user_id
    ).and_return_future(None)

    response = yield http_client.fetch(
        url,
        method="PUT",
        body=json.dumps({
            "access_token": access_token.access_token,
            "plate": plate,
            "latitude": latitude,
            "longitude": longitude,
        })
    )

    assert response.code == 200
    body = json.loads(response.body)
    _parking_space = body.get('parking_space')
    assert _parking_space['plate'] == parking_space.plate
    assert _parking_space['longitude'] == parking_space.location.longitude
    assert _parking_space['latitude'] == parking_space.location.latitude

    assert _parking_space.get('level') == parking_space.location.level
    assert _parking_space.get('address') == parking_space.location.location


@pytest.mark.gen_test
def test_post_parking_space_with_non_checked_in_vehicle(http_client, base_url, access_token):
    vehicle = Vehicle.get_mock_object()
    user = User.get_mock_object(overrides={"owned_vehicles": None})
    expect(module.UserService).get_user_detail(user_id=user.user_id).and_return_future(user)
    result = yield module._verify_vehicle_belonging(user_id=user.user_id, plate=vehicle.plate)
    assert not result

    user = User.get_mock_object(overrides={"owned_vehicles": [vehicle]})
    expect(module.UserService).get_user_detail(user_id=user.user_id).and_return_future(user)
    result = yield module._verify_vehicle_belonging(user_id=user.user_id, plate=vehicle.plate)
    assert result

    another = Vehicle.get_mock_object()
    user = User.get_mock_object(overrides={"owned_vehicles": [vehicle, another]})
    expect(module.UserService).get_user_detail(user_id=user.user_id).and_return_future(user)
    result = yield module._verify_vehicle_belonging(user_id=user.user_id, plate=vehicle.plate)
    assert result

    another = Vehicle.get_mock_object()
    user = User.get_mock_object(overrides={"owned_vehicles": [vehicle, another]})
    expect(module.UserService).get_user_detail(user_id=user.user_id).and_return_future(user)
    result = yield module._verify_vehicle_belonging(user_id=user.user_id, plate='00000')
    assert not result
