import pytest

from doubles import expect

from ParkingFinder.entities.access_token import AccessToken
from ParkingFinder.entities.user import User
from ParkingFinder.services import user as module


@pytest.mark.gen_test
def test_login():
    mocked_access_token = AccessToken.get_mock_object()
    mocked_user = User.get_mock_object({'user_id': mocked_access_token.user_id})

    expect(module.AccessTokenRepository).upsert(
        access_token=mocked_access_token.access_token,
        expires_at=mocked_access_token.expires_at,
        user_id=mocked_access_token.user_id,
        issued_at=mocked_access_token.issued_at,
    ).and_return_future(mocked_access_token)

    expect(module.UserService).get_user_detail(
        user_id=mocked_access_token.user_id
    ).and_return_future(mocked_user)

    user = yield module.UserService.login(access_token=mocked_access_token)
    assert user == mocked_user


@pytest.mark.gen_test
def test_register():
    mocked_user = User.get_mock_object()
    expect(module.UserRepository).upsert(user=mocked_user).and_return_future(mocked_user)
    user = yield module.UserService.register(user=mocked_user)
    assert user == mocked_user


@pytest.mark.gen_test
def test_logout():
    mocked_token = AccessToken.get_mock_object()
    expect(module.AccessTokenRepository).remove(
        access_token=mocked_token.access_token
    ).and_return_future(1)

    yield module.UserService.logout(access_token=mocked_token.access_token)


@pytest.mark.gen_test
def test_logout_with_access_token_not_exist():
    mocked_token = AccessToken.get_mock_object()
    expect(module.AccessTokenRepository).remove(
        access_token=mocked_token.access_token
    ).and_raise(module.NoResultFound)

    with pytest.raises(module.NotFound):
        yield module.UserService.logout(access_token=mocked_token.access_token)


@pytest.mark.gen_test
def test_get_user_detail():
    mocked_user = User.get_mock_object()
    expect(module.UserRepository).read_one(
        user_id=mocked_user.user_id
    ).and_return_future(mocked_user)

    user = yield module.UserService.get_user_detail(
        user_id=mocked_user.user_id
    )

    assert user == mocked_user


@pytest.mark.gen_test
def test_get_user_detail_with_user_not_exist():
    mocked_user = User.get_mock_object()
    expect(module.UserRepository).read_one(
        user_id=mocked_user.user_id
    ).and_raise(module.UserNotFound)

    with pytest.raises(module.NotFound):
        yield module.UserService.get_user_detail(
            user_id=mocked_user.user_id
        )
