import pytest
import json
import googleapiclient

from unittest.mock import MagicMock
from src.log import Logger


@pytest.fixture(scope='class')
def api_comment_response():
    response = {}

    with open('test_comment_api_response.json', 'r') as f:
        response = json.load(f)

    return response


@pytest.fixture
def logger():
    return Logger('debug')


@pytest.fixture
def mock_google_http_request(api_comment_response):
    mock = googleapiclient.http.HttpRequest
    mock.execute = MagicMock(return_value=api_comment_response)
