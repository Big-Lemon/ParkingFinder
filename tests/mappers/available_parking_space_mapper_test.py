from ParkingFinder.mappers import available_parking_space_mapper as module
from ParkingFinder.entities.location import Location

def test_mapper():

    available_parking_space = module.AvailableParkingSpace.get_mock_object()
    del available_parking_space.location['location'], available_parking_space.location['level']
    model = module.AvailableParkingSpacePool(
        plate=available_parking_space.plate,
        longitude=available_parking_space.location.longitude,
        latitude=available_parking_space.location.latitude,
        is_active=available_parking_space.is_active,
        created_at=available_parking_space.created_at,
        updated_at=available_parking_space.updated_at,
    )
    entity = module.AvailableParkingSpaceMapper.to_entity(model)
    assert available_parking_space == entity
    model = module.AvailableParkingSpaceMapper.to_model(entity)
    assert model.plate == entity.plate
    assert model.longitude == entity.location.longitude
    assert model.latitude == entity.location.latitude
    assert model.is_active == entity.is_active
    assert model.created_at == entity.created_at
    assert model.updated_at == entity.updated_at

    record = module.AvailableParkingSpaceMapper.to_record(available_parking_space)
    assert available_parking_space.to_primitive() == record
