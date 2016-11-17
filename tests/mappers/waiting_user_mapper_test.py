from ParkingFinder.mappers import waiting_user_mapper as module
from ParkingFinder.entities.location import Location

def test_mapper():

    waiting_user = module.WaitingUser.get_mock_object()
    del waiting_user.location['location'], waiting_user.location['level']

    model = module.WaitingUsers(
        user_id=waiting_user.user_id,
        longitude=waiting_user.location.longitude,
        latitude=waiting_user.location.latitude,
        is_active=waiting_user.is_active,
        created_at=waiting_user.created_at,
    )
    entity = module.WaitingUserMapper.to_entity(model)
    assert waiting_user == entity
    model = module.WaitingUserMapper.to_model(entity)
    assert model.user_id == entity.user_id
    assert model.longitude == entity.location.longitude
    assert model.latitude == entity.location.latitude
    assert model.is_active == entity.is_active
    assert model.created_at == entity.created_at

    record = module.WaitingUserMapper.to_record(waiting_user)
    assert waiting_user.to_primitive() == record
