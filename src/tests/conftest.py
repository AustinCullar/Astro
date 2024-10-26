import pytest
import json
import googleapiclient
import logging

import pandas as pd
import src.tests.test_api_responses as api_responses
from unittest.mock import MagicMock
from src.log import AstroLogger
from src.theme import AstroTheme


@pytest.fixture(scope='function')
def comment_dataframe():
    df = pd.DataFrame(columns=['comment_id', 'comment', 'user', 'date', 'visible'])

    df.loc[0] = ['UgyMLcxXS1Id2SaBuJd4AaABAg',
                 'hello there',
                 '@user1',
                 '2022-10-23T19:05:89Z',
                 1]

    df.loc[1] = ['UgwJuUmFZtOgkjrCrlp4AaABAg',
                 'this is terrible',
                 '@user2',
                 '2023-10-23T20:05:89Z',
                 1]

    df.loc[2] = ['UgwJuUmFZtOgkjrCrlp4AaABAg.A9Y4JkqJXpPA9Y4Z0_I_BA',
                 'this is awesome!',
                 '@user3',
                 '2021-8-23T20:11:90Z',
                 1]

    return df


@pytest.fixture(scope='function')
def api_comment_response():
    return json.loads(api_responses.test_comment_api_response)


@pytest.fixture(scope='function')
def api_video_response():
    return json.loads(api_responses.test_video_api_response, strict=True)


@pytest.fixture(scope='class')
def astro_theme():
    return AstroTheme()


@pytest.fixture(scope='class')
def logger(astro_theme):
    logging.setLoggerClass(AstroLogger)
    astro_logger = logging.getLogger(__name__)
    astro_logger.astro_config('debug', astro_theme)
    return astro_logger


@pytest.fixture(scope='function')
def mock_comment_google_http_request(api_comment_response):
    mock = googleapiclient.http.HttpRequest
    mock.execute = MagicMock(return_value=api_comment_response)


@pytest.fixture(scope='function')
def mock_video_google_http_request(api_video_response):
    mock = googleapiclient.http.HttpRequest
    mock.execute = MagicMock(return_value=api_video_response)
