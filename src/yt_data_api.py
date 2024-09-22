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

	"""
	Collect and store comment information in a dataframe. Collected
	info includes:

	* Username
	* Comment text
	* Publish date

	"""
	def get_comments(self, video_id: str) -> pd.DataFrame:
		comments = []
		youtube = build('youtube', 'v3', developerKey=self.api_key)

		request = youtube.commentThreads().list(
			part="snippet,replies",
			videoId=video_id,
			textFormat="plainText")

		df_index = 0
		df = pd.DataFrame(columns=['comment', 'user', 'date'])

		while request:
			replies = []
			comments = []
			dates = []
			user_names = []

			try:
				response = request.execute()

				for item in response['items']:
					#self.logger.debug('item: {}'.format(item))
					has_replies = 0 != item['snippet']['totalReplyCount']
					comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
					user = item['snippet']['topLevelComment']['snippet']['authorDisplayName']
					date = item['snippet']['topLevelComment']['snippet']['publishedAt']

					df.loc[df_index] = [comment, user, date]
					df_index += 1

					comments.append((user, comment, date))

					if has_replies:
						for reply in item['replies']['comments']:
							comment = reply['snippet']['textDisplay']
							user = reply['snippet']['authorDisplayName']
							date = reply['snippet']['publishedAt']

							df.loc[df_index] = [comment, user, date]
							df_index += 1

							comments.append((user, comment, date))
				break

			except Exception as e:
				self.logger.error(str(e))
				self.logger.error(traceback.format_exc())
				break

		return df
