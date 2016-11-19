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
    matched_parking_space_list.sort(key=lambda x: x.user_id)
    entity1 = yield module.MatchedParkingList.read_one('ANRCHST')
    entity2 = yield module.MatchedParkingList.read_one('4JTY881')
    expected_list = [entity1, entity2]
    expected_list.sort(key=lambda x: x.user_id)
    assert matched_parking_space_list == expected_list


@pytest.mark.gen_test
def test_read_many_with_one_result():
    matched_parking_space_list = yield module.MatchedParkingList.read_many('valid_account_1')
    for matched_parking_space in matched_parking_space_list:
        matched_parking_space.validate()
    assert len(matched_parking_space_list) == 1
    matched_parking_space_list.sort()
    entity = yield module.MatchedParkingList.read_one('6TRJ224')
    expected_list = [entity]
    expected_list.sort()
    assert matched_parking_space_list == expected_list


@pytest.mark.gen_test
def test_read_many_with_no_result():
    expect(module.MatchedParkingSpaceMapper).to_entity.never()
    matched_parking_space_list = yield module.MatchedParkingList.read_many('TANG')
    assert len(matched_parking_space_list) == 0


@pytest.mark.gen_test
def test_update():
    matched_parking_space = yield module.MatchedParkingList.update('valid_account', '6ELA725', 'rejected')
    assert matched_parking_space.status == 'rejected'
    _matched_parking_space = yield module.MatchedParkingList.read_one('6ELA725')
    assert matched_parking_space == _matched_parking_space

@pytest.mark.gen_test
def test_insert():
    mocked_space = MatchedParkingSpace.get_mock_object(overrides={
        'user_id': 'expired_account',
        'plate': '6DAY434',
        'status': 'awaiting',
    })
    matched_parking_space = yield module.MatchedParkingList.insert(mocked_space)
    _matched_parking_space = yield module.MatchedParkingList.read_one(plate=mocked_space.plate)
    del matched_parking_space['created_at'], _matched_parking_space['created_at']
    assert matched_parking_space == _matched_parking_space


@pytest.mark.gen_test
def test_remove():
    matched_parking_space = yield module.MatchedParkingList.read_one(plate='6DAY434')
    _matched_parking_space = yield module.MatchedParkingList.remove(plate='6DAY434')
    del matched_parking_space['created_at'], _matched_parking_space['created_at']
    assert matched_parking_space == _matched_parking_space
    expect(module.MatchedParkingSpaceMapper).to_entity.never()
    with pytest.raises(NoResultFound):
        yield module.MatchedParkingList.read_one(plate='6DAY434')


@pytest.mark.gen_test
def test_remove_with_no_result():
    expect(module.MatchedParkingSpaceMapper).to_entity.never()
    with pytest.raises(NoResultFound):
        yield module.MatchedParkingList.remove(plate='6DAY434')