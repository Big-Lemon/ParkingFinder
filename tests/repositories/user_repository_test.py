import pytest

from doubles import expect
from schematics.exceptions import ValidationError
from sqlalchemy.orm.exc import NoResultFound

from ParkingFinder.repositories import user_repository as module
from ParkingFinder.entities.user import User


@pytest.mark.gen_test
def test_read_one():
    user = yield module.UserRepository.read_one(user_id='valid_account_2')
    user.validate()
    assert user.user_id == 'valid_account_2'
    assert user.first_name == 'valid'
    assert user.last_name == 'account_2'
    assert not user.profile_picture_url


@pytest.mark.gen_test
def test_read_one_with_no_result():
    expect(module.UserMapper).to_entity.never()
    with pytest.raises(NoResultFound):
        yield module.UserRepository.read_one(user_id='hong')


@pytest.mark.gen_test
def test_upsert():
    mocked_user = User.get_mock_object()

    user = yield module.UserRepository.upsert(user=mocked_user)
    _user = yield module.UserRepository.read_one(user_id=mocked_user.user_id)
    assert user == _user

    user.activated_vehicle = '1234567'
    yield module.UserRepository.upsert(user)
    user = yield module.UserRepository.read_one(user_id=user.user_id)
    assert user.activated_vehicle == '1234567'


@pytest.mark.gen_test
def test_upsert_with_incomplete_entity():
    mocked_user = User({'user_id': '123'})
    # missing name
    with pytest.raises(ValidationError):
        yield module.UserRepository.upsert(user=mocked_user)
