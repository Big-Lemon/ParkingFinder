from ParkingFinder.mappers import user_mapper as module


def test_mapper():

    user = module.User.get_mock_object()
    params = user.to_primitive()
    del params['activated_vehicle']
    user = module.User(params)

    model = module.Users(
        user_id=user.user_id,
        first_name=user.first_name,
        last_name=user.last_name,
        profile_picture_url=user.profile_picture_url,
    )
    # activated_vehicle is None because it is not required
    entity = module.UserMapper.to_entity(model)
    assert user == entity

    model = module.UserMapper.to_model(entity)
    assert model.user_id == entity.user_id
    assert model.first_name == entity.first_name
    assert model.last_name == entity.last_name
    assert model.profile_picture_url == entity.profile_picture_url
    assert not model.activated_vehicle

    record = module.UserMapper.to_record(user)
    assert user.to_primitive() == record


