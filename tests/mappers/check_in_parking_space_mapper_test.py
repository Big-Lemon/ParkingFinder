from datetime import datetime

from ParkingFinder.mappers import parking_space_mapper as module


def test_mapper():

    parking_space = module.ParkingSpace.get_mock_object()
    params = parking_space.to_primitive()
    del params['level'], params['description']
    # change date format from %Y-%m-%d %H:%M:%S.%f to %Y-%m-%dT%H:%M:%S.%f
    # otherwise, it cannot be converted to model without errors
    date_object = datetime.strptime(params['created_at'], '%Y-%m-%d %H:%M:%S.%f')
    new_format = date_object.strftime('%Y-%m-%dT%H:%M:%S.%f')
    params['created_at'] = new_format

    parking_space = module.ParkingSpace(params)

    model = module.CheckInParkingSpace(
        user_id=parking_space.user_id,
        latitude=parking_space.latitude,
        longitude=parking_space.longitude,
        created_at=parking_space.created_at,
    )
    entity = module.CheckInParkingSpaceMapper.to_entity(model)
    assert parking_space == entity

    _model = module.CheckInParkingSpaceMapper.to_model(entity)
    # assert model == _model
    assert model.user_id == _model.user_id
    assert model.latitude == _model.latitude
    assert model.longitude == _model.longitude
    assert model.created_at == _model.created_at
    assert model.level == _model.level
    assert model.description == model.description

    # check contents
    assert model.user_id == entity.user_id
    assert model.latitude == entity.latitude
    assert model.longitude == entity.longitude
    assert model.created_at == entity.created_at

    record = module.CheckInParkingSpaceMapper.to_record(parking_space)
    assert parking_space.to_primitive() == record