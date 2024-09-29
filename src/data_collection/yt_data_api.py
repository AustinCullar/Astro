"""
Functions for gathering data from YouTube.
"""

import pandas as pd
import traceback

from src.data_collection.data_structures import VideoData
from googleapiclient.discovery import build


class YouTubeDataAPI:
    logger = None
    api_key = None
    youtube = None

    def __init__(self, logger, api_key):
        self.logger = logger.get_logger()
        self.api_key = api_key
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)

    def parse_comment_api_response(self, response) -> pd.DataFrame:
        """
        Parse API response for comment query. This will grab all comments and their replies,
        storing the resulting data in a dataframe.
        """
        df_index = 0
        df = pd.DataFrame(columns=['comment', 'user', 'date'])

        for item in response['items']:
            has_replies = 0 != item['snippet']['totalReplyCount']

            comment_info = item['snippet']['topLevelComment']['snippet']
            comment = comment_info['textDisplay']
            user = comment_info['authorDisplayName']
            date = comment_info['publishedAt']

            df.loc[df_index] = [comment, user, date]
            df_index += 1

            if has_replies:
                for reply in item['replies']['comments']:
                    reply_data = reply['snippet']

                    comment = reply_data['textDisplay']
                    user = reply_data['authorDisplayName']
                    date = reply_data['publishedAt']

                    df.loc[df_index] = [comment, user, date]
                    df_index += 1

        return df

    def get_comments(self, video_data) -> pd.DataFrame:
        """
        Collect and store comment information in a dataframe. Collected
        info includes:

        * Username
        * Comment text
        * Publish date

        """
        request = self.youtube.commentThreads().list(
            part="snippet,replies",
            videoId=video_data.video_id,
            textFormat="plainText")

        comment_dataframe = None

        try:
            response = request.execute()
            comment_dataframe = self.parse_comment_api_response(response)

        except Exception as e:
            self.logger.error(str(e))
            self.logger.error(traceback.format_exc())

        return comment_dataframe

    def get_video_metadata(self, video_id: str) -> VideoData:
        """
        Collect video information provided a video ID.
        Return all data in a VideoData class for easy access.
        """
        return_data = VideoData()

        request = self.youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=video_id)

        try:
            response = request.execute()
            video_data = response['items'][0]['snippet']
            video_stats = response['items'][0]['statistics']

            return_data.video_id = video_id
            return_data.channel_id = video_data['channelId']
            return_data.channel_title = video_data['channelTitle']
            return_data.like_count = video_stats['likeCount']
            return_data.view_count = video_stats['viewCount']
            return_data.comment_count = video_stats['commentCount']

        except Exception as e:
            self.logger.error(str(e))
            self.logger.error(traceback.format_exc())

        return return_data
