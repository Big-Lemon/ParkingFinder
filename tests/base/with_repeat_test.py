import pytest

from doubles import expect
from tornado import gen
from tornado.gen import coroutine, Return

from ParkingFinder.base.with_repeat import with_repeat
from ParkingFinder.base import with_repeat as module


class TestWithRepeat:
    @staticmethod
    @coroutine
    def assert_false():
        raise AssertionError


@pytest.fixture
def test_with_repeat():
    def wrapper(timeout=None, repeat_times=None, repeat_exceptions=None, duration=None):

        @with_repeat(timeout=timeout, repeat_exceptions=repeat_exceptions, repeat_times=repeat_times, duration=duration)
        @coroutine
        def method():
            yield TestWithRepeat.assert_false()
        return method
    return wrapper


@pytest.mark.gen_test
def test_with_repeat_with_no_arguments(test_with_repeat):

    expect(TestWithRepeat).assert_false.exactly(1).time.and_raise(AssertionError)
    expect(module).sleep.never()
    with pytest.raises(AssertionError):
        method = test_with_repeat()
        yield method()


@pytest.mark.gen_test
def test_with_repeat_with_repeat_times(test_with_repeat):
    expect(TestWithRepeat).assert_false.exactly(3).times.and_raise(AssertionError)
    expect(module).sleep.never()

    with pytest.raises(module.Timeout):
        method = test_with_repeat(repeat_times=3, repeat_exceptions=AssertionError)
        yield method()


@pytest.mark.gen_test
def test_with_repeat_with_unexpected_exception(test_with_repeat):
    expect(TestWithRepeat).assert_false.exactly(1).times.and_raise(AssertionError)
    expect(module).sleep.never()

    with pytest.raises(AssertionError):
        method = test_with_repeat(repeat_times=3, repeat_exceptions=ArithmeticError)
        yield method()


@pytest.mark.gen_test
def test_with_repeat_with_duration(test_with_repeat):
    expect(TestWithRepeat).assert_false.exactly(3).times.and_raise(AssertionError)
    expect(module).sleep.with_args(duration=1).exactly(3).and_return_future(None)

    with pytest.raises(module.Timeout):
        method = test_with_repeat(duration=1, repeat_times=3, repeat_exceptions=AssertionError)
        yield method()
