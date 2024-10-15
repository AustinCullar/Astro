import pytest
import json
import googleapiclient
import logging

import pandas as pd
from unittest.mock import MagicMock
from src.log import AstroLogger
import src.tests.test_api_responses as api_responses


@pytest.fixture(scope='class')
def comment_dataframe():
    df = pd.DataFrame(columns=['comment', 'user', 'date'])

    df.loc[0] = ['hello there', '@user1', '2022-10-23T19:05:89Z']
    df.loc[1] = ['this is terrible', '@user2', '2023-10-23T20:05:89Z']
    df.loc[2] = ['this is awesome!', '@user3', '2021-8-23T20:11:90Z']

    return df


@pytest.fixture(scope='function')
def api_comment_response():
    return json.loads(api_responses.test_comment_api_response)


@pytest.fixture(scope='function')
def api_video_response():
    return json.loads(api_responses.test_video_api_response, strict=True)


@pytest.fixture(scope='class')
def logger():
    logging.setLoggerClass(AstroLogger)
    astro_logger = logging.getLogger(__name__)
    astro_logger.astro_config('debug')
    return astro_logger


@pytest.fixture(scope='function')
def mock_comment_google_http_request(api_comment_response):
    mock = googleapiclient.http.HttpRequest
    mock.execute = MagicMock(return_value=api_comment_response)


@pytest.fixture(scope='function')
def mock_video_google_http_request(api_video_response):
    mock = googleapiclient.http.HttpRequest
    mock.execute = MagicMock(return_value=api_video_response)
