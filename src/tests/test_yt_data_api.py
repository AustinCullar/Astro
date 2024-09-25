"""
Tests for the YouTubeDataAPI class.
"""
import pytest

# Astro modules
from src.data_collection.yt_data_api import YouTubeDataAPI


def parametrize_api_comment_response(
        json_response,
        videoId='',
        textDisplay='',
        publishedAt='',
        authorDisplayName='',
        replyTextDisplay='',
        replyAuthorDisplayName=''):

    if videoId:
        json_response['items'][0]['snippet']['videoId'] = videoId

    if textDisplay:
        json_response['items'][0]['snippet']['topLevelComment']['snippet']['textDisplay'] = textDisplay

    if publishedAt:
        json_response['items'][0]['snippet']['topLevelComment']['snippet']['publishedAt'] = publishedAt

    if authorDisplayName:
        json_response['items'][0]['snippet']['topLevelComment']['snippet']['authorDisplayName'] = authorDisplayName

    if replyTextDisplay:
        json_response['items'][0]['replies']['comments'][0]['snippet']['textDisplay'] = replyTextDisplay

    if replyAuthorDisplayName:
        json_response['items'][0]['replies']['comments'][0]['snippet']['authorDisplayName'] = replyAuthorDisplayName

    return json_response


class TestYouTubeDataAPI:
    @pytest.mark.parametrize('textDisplay', ['hello', 'goodbye', '1234'])
    @pytest.mark.parametrize('publishedAt', ['2024-09-23T19:06:29Z', '2020-11-28T20:12:44Z', '2022-10-23T19:05:89Z'])
    @pytest.mark.parametrize('authorDisplayName', ['@test_user1', '@user-1234', '@best.youtuber'])
    @pytest.mark.parametrize('replyTextDisplay', ['reply text', 'hello 12345', 'test/reply'])
    @pytest.mark.parametrize('replyAuthorDisplayName', ['@test_replier1', '@test-replier1234', '@best.replier'])
    def test_get_comments(
            self,
            logger,
            api_comment_response,
            mock_google_http_request,
            textDisplay,
            publishedAt,
            authorDisplayName,
            replyTextDisplay,
            replyAuthorDisplayName):

        youtube = YouTubeDataAPI(logger, 'test_apikey')

        api_comment_response = parametrize_api_comment_response(
            api_comment_response,
            textDisplay=textDisplay,
            publishedAt=publishedAt,
            authorDisplayName=authorDisplayName,
            replyTextDisplay=replyTextDisplay,
            replyAuthorDisplayName=replyAuthorDisplayName)

        df = youtube.get_comments('test_videoid')

        assert not df.empty

        """
        The test data will only generate 2 rows in the dataframe:
        one for the parent comment and one for the reply.
        """
        for index, row in df.iterrows():
            if index == 0:  # parent comment
                assert textDisplay == row['comment']
                assert publishedAt == row['date']
                assert authorDisplayName == row['user']
            else:  # reply comment
                assert replyTextDisplay == row['comment']
                assert replyAuthorDisplayName == row['user']
