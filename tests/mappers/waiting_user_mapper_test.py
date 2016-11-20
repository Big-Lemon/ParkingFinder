import datetime
from ParkingFinder.mappers import waiting_user_mapper as module


def test_mapper():

    waiting_user = module.WaitingUser.get_mock_object(overrides={
        'user_id': '123',
        'is_active': True,
        'location': {
            'longitude': 123.123,
            'latitude': 45.123,
        },
    })
    record = module.WaitingUserMapper.to_record(entity=waiting_user)

    assert record['user_id'] == '123'
    assert record['longitude'] == 123.123
    assert record['latitude'] == 45.123
    assert record['created_at'] == str(waiting_user.created_at)

    _record = {
        'user_id': '123',
        'is_active': True,
        'longitude': 123.123,
        'latitude': 45.123,
        'created_at': str(datetime.datetime.utcnow())
    }
    entity = module.WaitingUserMapper.to_entity(record=_record)
    assert entity.user_id == _record['user_id']
    assert entity.is_active == _record['is_active']
    assert entity.location.longitude == _record['longitude']
    assert entity.location.latitude == _record['latitude']
    assert str(entity.created_at) == _record['created_at']
