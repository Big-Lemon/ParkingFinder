import pytest

from doubles import expect
from datetime import datetime
from schematics.exceptions import ValidationError
from sqlalchemy.orm.exc import NoResultFound

from ParkingFinder.entities.matched_parking_space import MatchedParkingSpace
from ParkingFinder.repositories import matched_parking_list as module


@pytest.mark.gen_test
def test_read_one():
    matched_parking_space = yield module.MatchedParkingList.read_one(plate='6ELA725')
    matched_parking_space.validate()
    assert matched_parking_space.user_id == 'valid_account'
    assert matched_parking_space.status == 'awaiting'
    assert matched_parking_space.created_at == datetime(2016, 11, 12, 10, 15, 5)


@pytest.mark.gen_test
def test_read_one_with_no_result():
    expect(module.MatchedParkingSpaceMapper).to_entity.never()
    with pytest.raises(NoResultFound):
        yield module.MatchedParkingList.read_one(plate='TML1234')


@pytest.mark.gen_test
def test_read_many_with_multiple_result():
    matched_parking_space_list = yield module.MatchedParkingList.read_many('valid_account_2')
    for matched_parking_space in matched_parking_space_list:
        matched_parking_space.validate()
    assert len(matched_parking_space_list) == 2
    matched_parking_space_list.sort()
    entity1 = yield module.MatchedParkingList.read_one('ANRCHST')
    entity2 = yield module.MatchedParkingList.read_one('4JTY881')
    expected_list = [entity1, entity2]
    expected_list.sort()
    assert matched_parking_space_list == expected_list


@pytest.mark.gen_test
def test_read_many_with_one_result():
    matched_parking_space_list = yield module.MatchedParkingList.read_many('valid_account_2')
    for matched_parking_space in matched_parking_space_list:
        matched_parking_space.validate()
    assert len(matched_parking_space_list) == 2
    matched_parking_space_list.sort()
    entity1 = yield module.MatchedParkingList.read_one('ANRCHST')
    entity2 = yield module.MatchedParkingList.read_one('4JTY881')
    expected_list = [entity1, entity2]
    expected_list.sort()
    assert matched_parking_space_list == expected_list

#
# @pytest.mark.gen_test
# def test_upsert():
#     mocked_user = User.get_mock_object(overrides={
#         "activated_vehicle": None
#     })
#
#     user = yield module.UserRepository.upsert(user=mocked_user)
#     _user = yield module.UserRepository.read_one(user_id=mocked_user.user_id)
#     assert user == _user
#
#     user.activated_vehicle = '1234567'
#     yield module.UserRepository.upsert(user)
#     user = yield module.UserRepository.read_one(user_id=user.user_id)
#     assert user.activated_vehicle == '1234567'
#
#
# @pytest.mark.gen_test
# def test_upsert_with_incomplete_entity():
#     mocked_user = User({'user_id': '123'})
#     # missing name
#     with pytest.raises(ValidationError):
#         yield module.UserRepository.upsert(user=mocked_user)
#
#
# @pytest.mark.gen_test
# def test_insert():
#     mocked_user = User.get_mock_object()
#     user = yield module.UserRepository._insert(user=mocked_user)
#     assert mocked_user == user