import pytest
from tornado.httpclient import HTTPClient
from clay import config


@pytest.fixture
def url():
    return config.get('url')


@pytest.fixture
def client():
    return HTTPClient()
