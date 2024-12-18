"""
Tests for the YouTubeDataAPI class.
"""
import pytest

# Astro modules
from src.data_collection.data_structures import VideoData
from src.data_collection.yt_data_api import YouTubeDataAPI


def parametrize_api_comment_response(
        json_response,
        videoId='',
        textDisplay='',
        publishedAt='',
        authorDisplayName='',
        replyTextDisplay='',
        replyAuthorDisplayName='',
        commentID=''):

    if videoId:
        json_response['items'][0]['snippet']['videoId'] = videoId

    if commentID:
        json_response['items'][0]['id'] = commentID

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


def parametrize_api_video_response(
        json_response,
        channelId='',
        channelTitle='',
        likeCount='',
        viewCount='',
        commentCount=''):

    if channelId:
        json_response['items'][0]['snippet']['channelId'] = channelId

    if channelTitle:
        json_response['items'][0]['snippet']['channelTitle'] = channelTitle

    if likeCount:
        json_response['items'][0]['statistics']['likeCount'] = likeCount

    if viewCount:
        json_response['items'][0]['statistics']['viewCount'] = viewCount

    if commentCount:
        json_response['items'][0]['statistics']['commentCount'] = commentCount

    return json_response


class TestYouTubeDataAPI:
    @pytest.mark.parametrize('textDisplay', ['hello', 'goodbye', '1234'])
    @pytest.mark.parametrize('publishedAt', ['2024-09-23T19:06:29Z', '2020-11-28T20:12:44Z', '2022-10-23T19:05:89Z'])
    @pytest.mark.parametrize('authorDisplayName', ['@test_user1', '@user-1234', '@best.youtuber'])
    @pytest.mark.parametrize('replyTextDisplay', ['reply text', 'hello 12345', 'test/reply'])
    @pytest.mark.parametrize('replyAuthorDisplayName', ['@test_replier1', '@test-replier1234', '@best.replier'])
    @pytest.mark.parametrize('commentID',
                             ['UgyMLcxXS1Id2SaBuJd4AaABAg',
                              'UgwJuUmFZtOgkjrCrlp4AaABAg',
                              'UgwJuUmFZtOgkjrCrlp4AaABAg.A9Y4JkqJXpPA9Y4Z0_I_BA'])
    def test_get_comments(
            self,
            logger,
            api_comment_response,
            mock_comment_google_http_request,
            textDisplay,
            publishedAt,
            authorDisplayName,
            replyTextDisplay,
            replyAuthorDisplayName,
            commentID):

        youtube = YouTubeDataAPI(logger, 'test_apikey')

        video_data = VideoData(
                video_id='video_id',
                channel_id='FvlvKP-khoFMOeyBzmXuaazd',
                channel_title='channel_title',
                view_count=123,
                like_count=123,
                comment_count=123)

        api_comment_response = parametrize_api_comment_response(
            api_comment_response,
            videoId=video_data.video_id,
            textDisplay=textDisplay,
            publishedAt=publishedAt,
            authorDisplayName=authorDisplayName,
            replyTextDisplay=replyTextDisplay,
            replyAuthorDisplayName=replyAuthorDisplayName,
            commentID=commentID)

        df = youtube.get_comments(video_data)

        assert not df.empty

        """
        The test data will only create 2 rows in the dataframe:
        one for the parent comment and one for the reply.
        """
        for index, row in df.iterrows():
            if index == 0:  # parent comment
                assert commentID == row['comment_id']
                assert textDisplay == row['comment']
                assert publishedAt == row['date']
                assert authorDisplayName == row['user']
            else:  # reply comment
                assert replyTextDisplay == row['comment']
                assert replyAuthorDisplayName == row['user']

    @pytest.mark.parametrize('channelId',
                             ['itXtJBHdZchKKjlnVrjXeCln',
                              'FvlvKP-khoFMOeyBzmXuaazd',
                              'LTO_OySEsmnRtoK-bkAeWXjW'])
    @pytest.mark.parametrize('channelTitle', ['YouTube_User', 'Test-User1'])
    @pytest.mark.parametrize('likeCount', ['0', '894', '11243'])
    @pytest.mark.parametrize('viewCount', ['0', '245', '66345'])
    @pytest.mark.parametrize('commentCount', ['0', '243', '76345'])
    def test_get_video_metadata(
            self,
            logger,
            api_video_response,
            mock_video_google_http_request,
            channelId,
            channelTitle,
            likeCount,
            viewCount,
            commentCount):

        youtube = YouTubeDataAPI(logger, 'test_apikey')

        api_video_response = parametrize_api_video_response(
                api_video_response,
                channelId=channelId,
                channelTitle=channelTitle,
                likeCount=likeCount,
                viewCount=viewCount,
                commentCount=commentCount)

        video_data = youtube.get_video_metadata('youtube.com/test/v=videoid')

        assert video_data.channel_id == channelId
        assert video_data.channel_title == channelTitle
        assert video_data.like_count == int(likeCount)
        assert video_data.view_count == int(viewCount)
        assert video_data.comment_count == int(commentCount)
