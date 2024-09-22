"""
Main entry point for Astro data collection. This program will
leverage the YouTube Data API to gather data from YouTube videos.
"""
import os

import pandas as pd

from dotenv import load_dotenv
from yt_data_api import YouTubeDataAPI
from sentiment import SentimentAnalysis
from log import Logger

def main():
	# load environment variables
	load_dotenv()
	api_key = os.getenv("API_KEY")
	log_level = os.getenv("LOG_LEVEL")

	# set up logging
	logger = Logger(log_level)
	log = logger.get_logger()

	# runescape video (needed low comment example)
	video_id="4M-FeqYmwdg"

	# pull comments from specified youtube video
	youtube = YouTubeDataAPI(logger, api_key)
	comments_df = youtube.get_comments(video_id)

	if not comments_df.empty:
		comments_df['PSentiment'] = ''
		comments_df['NSentiment'] = ''

		sa = SentimentAnalysis(logger)

		for index, row in comments_df.iterrows():
			sentiment = sa.get_sentiment(row['comment'])
			comments_df.loc[index, 'PSentiment'] = sentiment[0]
			comments_df.loc[index, 'NSentiment'] = sentiment[1]
		
	log.debug('Collected data preview: \n{}'.format(comments_df))

	# save comment data to csv file for now
	# TODO move data into a database
	comments_df.to_csv(f'{video_id}.csv')

if __name__ == "__main__":
	main()
