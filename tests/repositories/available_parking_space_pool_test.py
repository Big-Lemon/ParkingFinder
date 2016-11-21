import pytest
import redis as _redis

from sqlalchemy.orm.exc import NoResultFound

from ParkingFinder.entities.location import Location
from ParkingFinder.repositories import available_parking_space_pool as module
from ParkingFinder.base.redis_pool import redis_pool
from ParkingFinder.entities.available_parking_space import AvailableParkingSpace


@pytest.mark.gen_test
def test_insert_inactive():
    available_parking_space = AvailableParkingSpace.get_mock_object(
        overrides={
            'is_active': False
        }
    )
    _entity = yield module.AvailableParkingSpacePool.insert(
        available_parking_space=available_parking_space
    )

    redis = _redis.StrictRedis(connection_pool=redis_pool)
    try:
        coordinate = redis.geopos(module.COORDINATE, available_parking_space.plate)
    except TypeError:
        coordinate = []
    assert len(coordinate) == 0
    record = redis.hgetall(module.AVAILABLE_PARKING + available_parking_space.plate)
    assert record['plate'] == available_parking_space.plate
    assert record['latitude'] == str(available_parking_space.location.latitude)
    assert record['longitude'] == str(available_parking_space.location.longitude)
    assert record['expired_at'] == str(available_parking_space.expired_at)
    assert not record.get('is_active', None)


@pytest.mark.gen_test
def test_insert_active():
    available_parking_space = AvailableParkingSpace.get_mock_object(
        overrides={
            'is_active': True
        }
    )
    _entity = yield module.AvailableParkingSpacePool.insert(
        available_parking_space=available_parking_space
    )

    redis = _redis.StrictRedis(connection_pool=redis_pool)
    coordinate = redis.geopos(module.COORDINATE, available_parking_space.plate)
    assert len(coordinate) == 1
    assert "{0:.4f}".format(coordinate[0][0]) == \
           "{0:.4f}".format(available_parking_space.location.longitude)
    assert "{0:.4f}".format(coordinate[0][1]) == \
           "{0:.4f}".format(available_parking_space.location.latitude)

    record = redis.hgetall(module.AVAILABLE_PARKING + available_parking_space.plate)
    assert record['plate'] == available_parking_space.plate
    assert record['latitude'] == str(available_parking_space.location.latitude)
    assert record['longitude'] == str(available_parking_space.location.longitude)
    assert record['expired_at'] == str(available_parking_space.expired_at)
    assert not record.get('is_active', None)


@pytest.mark.gen_test
def test_read_one_inactive():
    available_parking_space = AvailableParkingSpace.get_mock_object(
        overrides={
            'is_active': False
        }
    )
    yield module.AvailableParkingSpacePool.insert(
        available_parking_space=available_parking_space
    )

    _parking_space = yield module.AvailableParkingSpacePool.read_one(
        plate=available_parking_space.plate
    )

    assert _parking_space.is_active == False
    assert _parking_space.plate == available_parking_space.plate
    assert _parking_space.expired_at == available_parking_space.expired_at
    assert _parking_space.location.latitude == available_parking_space.location.latitude
    assert _parking_space.location.longitude == available_parking_space.location.longitude


@pytest.mark.gen_test
def test_read_one_active():
    available_parking_space = AvailableParkingSpace.get_mock_object(
        overrides={
            'is_active': True
        }
    )
    yield module.AvailableParkingSpacePool.insert(
        available_parking_space=available_parking_space
    )

    _parking_space = yield module.AvailableParkingSpacePool.read_one(
        plate=available_parking_space.plate
    )

    assert _parking_space.is_active
    assert _parking_space.plate == available_parking_space.plate
    assert _parking_space.expired_at == available_parking_space.expired_at
    assert _parking_space.location.latitude == available_parking_space.location.latitude
    assert _parking_space.location.longitude == available_parking_space.location.longitude


@pytest.mark.gen_test
def test_update():
    available_parking_space = AvailableParkingSpace.get_mock_object(
        overrides={
            'is_active': True
        }
    )
    yield module.AvailableParkingSpacePool.insert(
        available_parking_space=available_parking_space
    )

    parking_space = yield module.AvailableParkingSpacePool.update(
        plate=available_parking_space.plate,
        is_active=False
    )

    assert parking_space.is_active == False

    location = Location.get_mock_object()
    yield module.AvailableParkingSpacePool.update(
        plate=available_parking_space.plate,
        is_active=True,
        location=location
    )

    p = yield module.AvailableParkingSpacePool.read_one(
        plate=available_parking_space.plate
    )
    assert p.location.latitude == location.latitude
    assert p.location.longitude == location.longitude


@pytest.mark.gen_test
def test_remove():
    available_parking_space = AvailableParkingSpace.get_mock_object(
        overrides={
            'is_active': True
        }
    )
    yield module.AvailableParkingSpacePool.insert(
        available_parking_space=available_parking_space
    )

    _parking_space = yield module.AvailableParkingSpacePool.remove(
        plate=available_parking_space.plate
    )
    assert _parking_space.is_active
    assert _parking_space.plate == available_parking_space.plate
    assert _parking_space.expired_at == available_parking_space.expired_at
    assert _parking_space.location.latitude == available_parking_space.location.latitude
    assert _parking_space.location.longitude == available_parking_space.location.longitude

    with pytest.raises(NoResultFound):
        yield module.AvailableParkingSpacePool.remove(
            plate=available_parking_space.plate
        )


@pytest.mark.gen_test
def test_pop_many():
    available_parking_spaces = [
        AvailableParkingSpace.get_mock_object(
            overrides={
                'plate': '0000000',
                'is_active': True,
                'location': {
                    'latitude': 10.00004,
                    'longitude': 50.0003
                }
            }
        ),
        AvailableParkingSpace.get_mock_object(
            overrides={
                'plate': '0000001',
                'is_active': True,
                'location': {
                    'latitude': 10.00002,
                    'longitude': 50.0003
                }
            }
        ),
        AvailableParkingSpace.get_mock_object(
            overrides={
                'plate': '0000002',
                'is_active': True,
                'location': {
                    'latitude': 10.00005,
                    'longitude': 50.0003
                }
            }
        )
    ]
    for parking_space in available_parking_spaces:
        yield module.AvailableParkingSpacePool.insert(
            available_parking_space=parking_space
        )

    spaces = yield module.AvailableParkingSpacePool.pop_many(
        latitude=10.00001,
        longitude=50.00002,
    )
    assert len(spaces) == 2
    first = spaces[0]
    second = spaces[1]
    assert first.plate == '0000001'
    assert second.plate == '0000000'
    assert first.location.latitude == available_parking_spaces[1].location.latitude
    assert first.location.longitude == available_parking_spaces[1].location.longitude
    assert second.location.latitude == available_parking_spaces[0].location.latitude
    assert second.location.longitude == available_parking_spaces[0].location.longitude

    for parking_space in available_parking_spaces:
        yield module.AvailableParkingSpacePool.insert(
            available_parking_space=parking_space
        )

    spaces = yield module.AvailableParkingSpacePool.pop_many(
        latitude=10.00001,
        longitude=50.00002,
        ignore_list=['0000001']
    )

    assert len(spaces) == 2
    first = spaces[0]
    second = spaces[1]
    assert first.plate == '0000000'
    assert second.plate == '0000002'
    assert first.location.latitude == available_parking_spaces[0].location.latitude
    assert first.location.longitude == available_parking_spaces[0].location.longitude
    assert second.location.latitude == available_parking_spaces[2].location.latitude
    assert second.location.longitude == available_parking_spaces[2].location.longitude
