"""
Functions for gathering data from YouTube.
"""

import pandas as pd
import traceback

from googleapiclient.discovery import build
from time import sleep

# for debugging purposes
import json

class YouTubeDataAPI:
	logger = None
	api_key = None

	def __init__(self, logger, api_key):
		self.logger = logger.get_logger()
		self.api_key = api_key

	def parse_comment_api_response(self, response) -> pd.DataFrame:
		"""
		Parse API response for comment query. This will grab all comments and their replies,
		storing the resulting data in a dataframe.
		"""
		df_index = 0
		df = pd.DataFrame(columns=['comment', 'user', 'date'])

		for item in response['items']:
			#self.logger.debug('item: {}'.format(item))
			has_replies = 0 != item['snippet']['totalReplyCount']
			comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
			user = item['snippet']['topLevelComment']['snippet']['authorDisplayName']
			date = item['snippet']['topLevelComment']['snippet']['publishedAt']

			df.loc[df_index] = [comment, user, date]
			df_index += 1

			if has_replies:
				for reply in item['replies']['comments']:
					comment = reply['snippet']['textDisplay']
					user = reply['snippet']['authorDisplayName']
					date = reply['snippet']['publishedAt']

					df.loc[df_index] = [comment, user, date]
					df_index += 1

		return df

	def get_comments(self, video_id: str) -> pd.DataFrame:
		"""
		Collect and store comment information in a dataframe. Collected
		info includes:

		* Username
		* Comment text
		* Publish date

		"""
		youtube = build('youtube', 'v3', developerKey=self.api_key)

		request = youtube.commentThreads().list(
			part="snippet,replies",
			videoId=video_id,
			textFormat="plainText")

		comment_dataframe = None

		while request:
			try:
				response = request.execute()
				comment_dataframe = self.parse_comment_api_response(response)
				break

			except Exception as e:
				self.logger.error(str(e))
				self.logger.error(traceback.format_exc())
				break

		return comment_dataframe
