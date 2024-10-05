"""
Functions for gathering data from YouTube.
"""

import pandas as pd
import traceback
import string

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

    @staticmethod
    def valid_video_id(video_id: str) -> bool:
        valid_tokens = (string.ascii_uppercase +
                        string.ascii_lowercase +
                        string.digits + '-' + '_')

        if video_id:
            for token in video_id:
                if token not in valid_tokens:
                    return False

            # all tokens are valid
            return True

        # null video_id
        return False

    def parse_comment_api_response(self, response, comment_dataframe) -> pd.DataFrame:
        """
        Parse API response for comment query. This will grab all comments and their replies,
        storing the resulting data in a dataframe.
        """
        # if the dataframe is non-null and not empty, we're appending data to the dataframe
        append_dataframe = comment_dataframe is not None and not comment_dataframe.empty

        if append_dataframe:
            df_index = len(comment_dataframe.index)  # last index in dataframe
            df = comment_dataframe
        else:  # create new dataframe
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

        comment_dataframe = None
        page_token = ''
        comment_count = video_data.comment_count
        unfetched_comments = True

        while unfetched_comments:
            # The API limits comment requests to 100 records
            max_comments = min(100, comment_count)

            self.logger.debug('collecting {} comments'.format(max_comments))

            request = self.youtube.commentThreads().list(
                part='snippet,replies',
                videoId=video_data.video_id,
                pageToken=page_token,
                maxResults=max_comments,
                textFormat='plainText')

            comment_count -= max_comments
            unfetched_comments = True if comment_count > 0 else False

            try:
                response = request.execute()
                comment_dataframe = self.parse_comment_api_response(response, comment_dataframe)
                if 'nextPageToken' in response:  # there are more comments to fetch
                    page_token = response['nextPageToken']
                else:
                    unfetched_comments = False

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
            return_data.like_count = int(video_stats['likeCount'])
            return_data.view_count = int(video_stats['viewCount'])
            return_data.comment_count = int(video_stats['commentCount'])

        except Exception as e:
            self.logger.error(str(e))
            self.logger.error(traceback.format_exc())

        return return_data
