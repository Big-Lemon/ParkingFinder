import pytest
import redis as _redis

from sqlalchemy.orm.exc import NoResultFound

from ParkingFinder.entities.location import Location
from ParkingFinder.repositories import waiting_user_pool as module
from ParkingFinder.base.redis_pool import redis_pool
from ParkingFinder.entities.waiting_user import WaitingUser


@pytest.mark.gen_test
def test_insert_inactive():
    waiting_user = WaitingUser.get_mock_object(
        overrides={
            'is_active': False
        }
    )
    _entity = yield module.WaitingUserPool.insert(
        waiting_user=waiting_user
    )

    redis = _redis.StrictRedis(connection_pool=redis_pool)
    try:
        coordinate = redis.geopos(module.COORDINATE, waiting_user.user_id)
    except TypeError:
        coordinate = []
    assert len(coordinate) == 0
    record = redis.hgetall(module.WAITING_USER + waiting_user.user_id)
    assert record['user_id'] == waiting_user.user_id
    assert record['latitude'] == str(waiting_user.location.latitude)
    assert record['longitude'] == str(waiting_user.location.longitude)
    assert record['created_at'] == str(waiting_user.created_at)
    assert not record.get('is_active', None)


@pytest.mark.gen_test
def test_insert_active():
    waiting_user = WaitingUser.get_mock_object(
        overrides={
            'user_id': 'hong',
            'is_active': True
        }
    )
    yield module.WaitingUserPool.insert(
        waiting_user=waiting_user
    )

    redis = _redis.StrictRedis(connection_pool=redis_pool)
    coordinate = redis.geopos(module.COORDINATE, waiting_user.user_id)
    assert len(coordinate) == 1
    assert "{0:.4f}".format(coordinate[0][0]) == \
           "{0:.4f}".format(waiting_user.location.longitude)
    assert "{0:.4f}".format(coordinate[0][1]) == \
           "{0:.4f}".format(waiting_user.location.latitude)

    record = redis.hgetall(module.WAITING_USER + waiting_user.user_id)
    assert record['user_id'] == waiting_user.user_id
    assert record['latitude'] == str(waiting_user.location.latitude)
    assert record['longitude'] == str(waiting_user.location.longitude)
    assert record['created_at'] == str(waiting_user.created_at)
    assert not record.get('is_active', None)


@pytest.mark.gen_test
def test_read_one_inactive():
    waiting_user = WaitingUser.get_mock_object(
        overrides={
            'user_id': 'fei',
            'is_active': False
        }
    )
    yield module.WaitingUserPool.insert(
        waiting_user=waiting_user
    )

    _waiting_user = yield module.WaitingUserPool.read_one(
        user_id=waiting_user.user_id
    )

    assert _waiting_user.is_active == False
    assert _waiting_user.user_id == waiting_user.user_id
    assert _waiting_user.created_at == waiting_user.created_at
    assert _waiting_user.location.latitude == waiting_user.location.latitude
    assert _waiting_user.location.longitude == waiting_user.location.longitude


@pytest.mark.gen_test
def test_read_one_active():
    waiting_user = WaitingUser.get_mock_object(
        overrides={
            'user_id': 'li',
            'is_active': True
        }
    )
    yield module.WaitingUserPool.insert(
        waiting_user=waiting_user
    )

    _waiting_user = yield module.WaitingUserPool.read_one(
        user_id=waiting_user.user_id
    )

    assert _waiting_user.is_active
    assert _waiting_user.user_id == waiting_user.user_id
    assert _waiting_user.created_at == waiting_user.created_at
    assert _waiting_user.location.latitude == waiting_user.location.latitude
    assert _waiting_user.location.longitude == waiting_user.location.longitude


@pytest.mark.gen_test
def test_update():
    waiting_user = WaitingUser.get_mock_object(
        overrides={
            'is_active': True
        }
    )
    yield module.WaitingUserPool.insert(
        waiting_user=waiting_user
    )

    waiting_user = yield module.WaitingUserPool.update(
        user_id=waiting_user.user_id,
        is_active=False
    )

    assert waiting_user.is_active == False

    location = Location.get_mock_object()
    yield module.WaitingUserPool.update(
        user_id=waiting_user.user_id,
        is_active=True,
        location=location
    )

    p = yield module.WaitingUserPool.read_one(
        user_id=waiting_user.user_id
    )
    assert p.location.latitude == location.latitude
    assert p.location.longitude == location.longitude


@pytest.mark.gen_test
def test_remove():
    waiting_user = WaitingUser.get_mock_object(
        overrides={
            'is_active': True
        }
    )
    yield module.WaitingUserPool.insert(
        waiting_user=waiting_user
    )

    _waiting_user = yield module.WaitingUserPool.remove(
        user_id=waiting_user.user_id
    )
    assert _waiting_user.is_active
    assert _waiting_user.user_id == waiting_user.user_id
    assert _waiting_user.created_at == waiting_user.created_at
    assert _waiting_user.location.latitude == waiting_user.location.latitude
    assert _waiting_user.location.longitude == waiting_user.location.longitude

    with pytest.raises(NoResultFound):
        yield module.WaitingUserPool.remove(
            user_id=waiting_user.user_id
        )


@pytest.mark.gen_test
def test_pop_one():
    waiting_users = [
        WaitingUser.get_mock_object(
            overrides={
                'user_id': '0000000',
                'is_active': True,
                'location': {
                    'latitude': 10.00004,
                    'longitude': 50.0003
                }
            }
        ),
        WaitingUser.get_mock_object(
            overrides={
                'user_id': '0000001',
                'is_active': True,
                'location': {
                    'latitude': 10.00002,
                    'longitude': 50.0003
                }
            }
        ),
        WaitingUser.get_mock_object(
            overrides={
                'user_id': '0000002',
                'is_active': True,
                'location': {
                    'latitude': 10.00005,
                    'longitude': 50.0003
                }
            }
        )
    ]
    for waiting_user in waiting_users:
        yield module.WaitingUserPool.insert(
            waiting_user=waiting_user
        )

    user = yield module.WaitingUserPool.pop_one(
        latitude=10.00001,
        longitude=50.00002,
    )
    first = user
    assert first.user_id == '0000001'
    assert first.location.latitude == waiting_users[1].location.latitude
    assert first.location.longitude == waiting_users[1].location.longitude

    for waiting_user in waiting_users:
        yield module.WaitingUserPool.insert(
            waiting_user=waiting_user
        )

    user = yield module.WaitingUserPool.pop_one(
        latitude=10.00001,
        longitude=50.00002,
        ignore_user_ids=['0000001']
    )

    first = user
    assert first.user_id == '0000000'
    assert first.location.latitude == waiting_users[0].location.latitude
    assert first.location.longitude == waiting_users[0].location.longitude
