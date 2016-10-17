import datetime
import pytest

from doubles import expect
from sqlalchemy.orm.exc import NoResultFound

from ParkingFinder.repositories import access_token_repository as module
from ParkingFinder.entities.access_token import AccessToken


@pytest.mark.gen_test
def test_read_one():
    token = yield module.AccessTokenRepository.read_one(access_token='100000')
    assert token.access_token == '100000'
    assert token.user_id == 'valid_account'


@pytest.mark.gen_test
def test_read_one_with_no_result():
    expect(module.AccessTokenMapper).to_entity.never()
    with pytest.raises(NoResultFound):
        yield module.AccessTokenRepository.read_one(access_token='invalid_token')


@pytest.mark.gen_test
def test_read_many():
    tokens = yield module.AccessTokenRepository.read_many(user_id='valid_account')
    sorted(tokens, key=lambda token: token.access_token)
    assert len(tokens) == 3
    assert tokens[0].access_token == '100000'
    assert tokens[1].access_token == '100001'
    assert tokens[2].access_token == '100002'


@pytest.mark.gen_test
def test_read_many_with_no_result():
    expect(module.AccessTokenMapper).to_entity.never()
    tokens = yield module.AccessTokenRepository.read_many(user_id='non-exist user')
    assert len(tokens) == 0


@pytest.mark.gen_test
def test_upsert():
    mocked_token = AccessToken.get_mock_object(overrides={'user_id': 'valid_account'})
    token = yield module.AccessTokenRepository.upsert(
        access_token=mocked_token.access_token,
        expires_at=mocked_token.expires_at,
        user_id=mocked_token.user_id,
        issued_at=mocked_token.issued_at,
    )

    assert mocked_token == token

    mocked_token.expires_at = datetime.datetime(2050, 12, 14, 5, 12, 31)

    yield module.AccessTokenRepository.upsert(
        access_token=mocked_token.access_token,
        expires_at=mocked_token.expires_at,
    )

    token = yield module.AccessTokenRepository.read_one(
        access_token=mocked_token.access_token
    )

    assert token.expires_at == datetime.datetime(2050, 12, 14, 5, 12, 31)
    assert token.user_id == mocked_token.user_id
    assert token.access_token == mocked_token.access_token
