"""
Functions for gathering data from YouTube.
"""
import pandas as pd
import traceback
import string
import json

from src.data_collection.data_structures import VideoData
from googleapiclient.discovery import build


class YouTubeDataAPI:
    logger = None
    api_key = None
    youtube = None
    log_json = False

    def __init__(self, logger, api_key, log_json=False):
        self.logger = logger
        self.api_key = api_key
        self.log_json = log_json
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)

    def __parse_comment_api_response(self, response, comment_dataframe) -> pd.DataFrame:
        """
        Parse API response for comment query. This will grab all comments and their replies,
        storing the resulting data in a dataframe.
        """
        # if the dataframe is non-null and not empty, we're appending data to the dataframe
        append_dataframe = comment_dataframe is not None and not comment_dataframe.empty

        comment_count = 0

        if append_dataframe:
            df_index = len(comment_dataframe.index)  # last index in dataframe
            df = comment_dataframe
        else:  # create new dataframe
            df_index = 0
            df = pd.DataFrame(columns=['comment_id', 'comment', 'user', 'date', 'visible'])

        for item in response['items']:
            has_replies = 0 != item['snippet']['totalReplyCount']

            comment_id = item['id']
            comment_info = item['snippet']['topLevelComment']['snippet']
            comment = comment_info['textDisplay']
            user = comment_info['authorDisplayName']
            date = comment_info['publishedAt']
            visible = True  # this is used to track comment visibility changes

            df.loc[df_index] = [comment_id, comment, user, date, visible]
            df_index += 1
            comment_count += 1

            if has_replies:
                for reply in item['replies']['comments']:
                    reply_data = reply['snippet']

                    comment_id = reply['id']
                    comment = reply_data['textDisplay']
                    user = reply_data['authorDisplayName']
                    date = reply_data['publishedAt']

                    df.loc[df_index] = [comment_id, comment, user, date, visible]
                    df_index += 1
                    comment_count += 1

        return df, comment_count

    def __extract_video_id_from_url(self, url: str) -> str:
        """
        Grab the video ID from the provided URL. The ID will come after
        the substring 'v=' in the URL, so I just split the string on that
        substring and return the latter half.
        """
        video_id = url.split('v=')[1]

        # validate extracted video id
        valid_tokens = (string.ascii_uppercase +
                        string.ascii_lowercase +
                        string.digits + '-' + '_')

        for token in video_id:
            if token not in valid_tokens:
                raise ValueError('Invalid video URL provided')

        return video_id

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
        unfetched_comments = True

        self.logger.debug('Downloading comments...')

        if 0 >= video_data.comment_count:
            self.logger.error(f'Received bad comment count: {video_data.comment_count}')
            return None

        with self.logger.progress_bar('Downloading comments', video_data.comment_count) as progress:
            while unfetched_comments:
                request = self.youtube.commentThreads().list(
                    part='snippet,replies',
                    videoId=video_data.video_id,
                    pageToken=page_token,
                    maxResults=100,  # API limit is 100
                    textFormat='plainText')

                try:
                    response = request.execute()
                    if self.log_json:
                        with self.logger.log_file_only():
                            self.logger.info(json.dumps(response, indent=4))

                    comment_dataframe, comments_added = self.__parse_comment_api_response(response, comment_dataframe)
                    if 'nextPageToken' in response:  # there are more comments to fetch
                        page_token = response['nextPageToken']
                    else:
                        self.logger.debug("Comment collection complete")
                        unfetched_comments = False

                    progress.advance(comments_added)

                except Exception as e:
                    self.logger.error(str(e))
                    self.logger.error(traceback.format_exc())

            # get filtered comment count by subtracting our collected count from our expected count
            filtered_comments = video_data.comment_count - len(comment_dataframe.index)
            if 0 < filtered_comments:
                video_data.filtered_comment_count = filtered_comments
            progress.complete()

        return comment_dataframe

    def get_video_metadata(self, url: str) -> VideoData:
        """
        Collect video information provided a video ID.
        Return all data in a VideoData class for easy access.
        """
        self.logger.debug('Collecting video metadata...')

        video_id = self.__extract_video_id_from_url(url)
        return_data = VideoData()

        request = self.youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=video_id)

        try:
            response = request.execute()
            if self.log_json:
                with self.logger.log_file_only():
                    self.logger.info(json.dumps(response, indent=4))

            video_data = response['items'][0]['snippet']
            video_stats = response['items'][0]['statistics']

            return_data.video_id = video_id
            return_data.video_title = video_data['title']
            return_data.channel_id = video_data['channelId']
            return_data.channel_title = video_data['channelTitle']
            return_data.like_count = int(video_stats['likeCount'])
            return_data.view_count = int(video_stats['viewCount'])
            if 'commentCount' in video_stats:
                return_data.comment_count = int(video_stats['commentCount'])
            else:
                return_data.comments_disabled = True

        except Exception as e:
            self.logger.error(str(e))
            self.logger.error(traceback.format_exc())

        return return_data
