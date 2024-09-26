import pytest
import json
import googleapiclient

import pandas as pd
from unittest.mock import MagicMock
from src.log import Logger


@pytest.fixture(scope='class')
def comment_dataframe():
    df = pd.DataFrame(columns=['comment', 'user', 'date'])

    df.loc[0] = ['hello there', '@user1', '2022-10-23T19:05:89Z']
    df.loc[1] = ['this is terrible', '@user2', '2023-10-23T20:05:89Z']
    df.loc[2] = ['this is awesome!', '@user3', '2021-8-23T20:11:90Z']

    return df


@pytest.fixture(scope='class')
def api_comment_response():
    response = {}

    with open('test_comment_api_response.json', 'r') as f:
        response = json.load(f)

    return response


@pytest.fixture(scope='class')
def logger():
    return Logger('debug')


@pytest.fixture(scope='class')
def mock_google_http_request(api_comment_response):
    mock = googleapiclient.http.HttpRequest
    mock.execute = MagicMock(return_value=api_comment_response)
