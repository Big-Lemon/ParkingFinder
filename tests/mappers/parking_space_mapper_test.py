from datetime import datetime

from ParkingFinder.mappers import parking_space_mapper as module


def test_mapper():

    parking_space = module.ParkingSpace.get_mock_object()
    params = parking_space.to_primitive()
    del params['location'], params['level']
    date_object = datetime.strptime(params['created_at'], '%Y-%m-%d %H:%M:%S.%f')
    new_format = date_object.strftime('%Y-%m-%dT%H:%M:%S.%f')
    params['created_at'] = new_format
    parking_space = module.ParkingSpace(params)

    model = module.ParkingLot(
        plate=parking_space.plate,
        latitude=parking_space.latitude,
        longitude=parking_space.longitude,
        created_at=parking_space.created_at,
    )

    entity = module.ParkingSpaceMapper.to_entity(model)
    assert parking_space == entity
    model = module.ParkingSpaceMapper.to_model(entity)
    assert model.plate == entity.plate
    assert model.latitude == entity.latitude
    assert model.longitude == entity.longitude
    assert model.created_at == entity.created_at

    record = module.ParkingSpaceMapper.to_record(parking_space)
    assert parking_space.to_primitive() == record
