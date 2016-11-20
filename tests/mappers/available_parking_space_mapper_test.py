from datetime import datetime
from ParkingFinder.mappers import available_parking_space_mapper as module


def test_mapper():

    now = datetime.utcnow()
    parking = module.AvailableParkingSpace.get_mock_object(overrides={
        'plate': '123',
        'is_active': True,
        'location': {
            'longitude': 123.123,
            'latitude': 45.123,
        },
        'distance': 100,
        'expired_at': now
    })
    record = module.AvailableParkingSpaceMapper.to_record(entity=parking)

    assert record['plate'] == '123'
    assert record['longitude'] == 123.123
    assert record['latitude'] == 45.123
    assert not record.get('is_active', None)
    assert not record.get('distance', None)
    assert record['expired_at'] == str(parking.expired_at)

    record = {
        'plate': '123',
        'is_active': True,
        'longitude': 123.123,
        'latitude': 45.123,
        'distance': 100,
        'expired_at': str(now)
    }
    entity = module.AvailableParkingSpaceMapper.to_entity(record=record)
    assert entity.plate == '123'
    assert entity.location.longitude == 123.123
    assert entity.location.latitude == 45.123
    assert entity.is_active
    assert entity.distance == 100
    assert entity.expired_at == now

