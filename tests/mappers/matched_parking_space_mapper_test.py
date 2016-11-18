from ParkingFinder.mappers import matched_parking_space_mapper as module


def test_mapper():

    matched_parking_space = module.MatchedParkingSpace.get_mock_object()
    model = module.MatchedParkingSpaceList(
        user_id=matched_parking_space.user_id,
        plate=matched_parking_space.plate,
        status=matched_parking_space.status,
        created_at=matched_parking_space.created_at,
    )
    entity = module.MatchedParkingSpaceMapper.to_entity(model)
    assert matched_parking_space == entity
    model = module.MatchedParkingSpaceMapper.to_model(entity)
    assert model.user_id == entity.user_id
    assert model.plate == entity.plate
    assert model.status == entity.status
    assert model.created_at == entity.created_at

    record = module.MatchedParkingSpaceMapper.to_record(matched_parking_space)
    assert matched_parking_space.to_primitive() == record
