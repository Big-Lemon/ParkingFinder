import pytest

from ParkingFinder.handlers.app import app as application


@pytest.fixture
def app():
    return application


@pytest.mark.gen_test
def test_health(http_client, base_url):
    response = yield http_client.fetch(base_url)
    assert response.code == 200
