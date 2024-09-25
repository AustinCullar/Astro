"""
Main entry point for Astro data collection. This program will
leverage the YouTube Data API to gather data from YouTube videos.
"""
import os
import argparse

import pandas as pd

from dotenv import load_dotenv
from data_collection.yt_data_api import YouTubeDataAPI
from data_collection.sentiment import SentimentAnalysis
from log import Logger
from astro_db import AstroDB

def extract_video_id_from_url(url: str) -> str:
    """
    Grab the video ID from the provided URL. The ID will come after
    the substring 'v=' in the URL, so I just split the string on that
    substring and return the latter half.
    """
    video_id = url.split('v=')[1]
    return video_id

def parse_args():
    """
    Argument parsing logic. Returns the arguments parsed from the CLI
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("youtube_url", type=str, help="URL to youtube video")
    parser.add_argument("-l", "--log", type=str, choices=['debug', 'info', 'warn', 'error'],
        help='Set the logging level')

    args = parser.parse_args()

    return args


def main():
    # parse arguments
    args = parse_args()
    video_id = extract_video_id_from_url(args.youtube_url)

    # load environment variables
    load_dotenv()

    # prioritize log level provided on CLI, fallback to env variable
    log_level = args.log if args.log else os.getenv("LOG_LEVEL")
    api_key = os.getenv("API_KEY")
    db_file = os.getenv("DB_FILE")

    # set up logging
    logger = Logger(log_level)
    log = logger.get_logger()

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

    # Database logic
    db = AstroDB(logger, db_file)
    db.create_database()
    db.insert_comment_dataframe(video_id, comments_df)

    log.debug('Collected data preview: \n{}'.format(comments_df))

if __name__ == "__main__":
    main()
