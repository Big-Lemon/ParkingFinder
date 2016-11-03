from ParkingFinder.mappers import parking_space_mapper as module


def test_mapper():

    parking_space = module.ParkingSpace.get_mock_object()
    params = parking_space.to_primitive()
    del params['level'], params['description']
    parking_space = module.ParkingSpace(params)

    model = module.CheckInParkingSpace(
        user_id=parking_space.user_id,
        latitude=parking_space.latitude,
        longitude=parking_space.longitude,
        created_at=parking_space.created_at,
    )
    entity = module.CheckInParkingSpaceMapper.to_entity(model)
    assert parking_space == entity

    model = module.CheckInParkingSpaceMapper.to_model(entity)
    assert model.user_id == entity.user_id
    assert model.latitude == entity.latitude
    assert model.longitude == entity.longitude

    record = module.CheckInParkingSpaceMapper.to_record(parking_space)
    assert parking_space.to_primitive() == record