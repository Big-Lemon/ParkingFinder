from ParkingFinder.mappers import access_token_mapper as module


def test_mapper():

    token = module.AccessToken.get_mock_object()
    model = module.AccessTokenModel(
        user_id=token.user_id,
        access_token=token.access_token,
        expires_at=token.expires_at,
        issued_at=token.issued_at,
    )
    entity = module.AccessTokenMapper.to_entity(model)
    assert token == entity

    model = module.AccessTokenMapper.to_model(entity)
    assert model.access_token == entity.access_token
    assert model.user_id == entity.user_id

    record = module.AccessTokenMapper.to_record(token)
    assert token.to_primitive() == record



