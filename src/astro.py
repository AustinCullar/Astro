"""
Main entry point for Astro data collection. This program will
leverage the YouTube Data API to gather data from YouTube videos.
"""
import os
import argparse

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

    parser.add_argument("youtube_url", type=str, help="youtube video URL")
    parser.add_argument("-l", "--log", type=str, choices=['debug', 'info', 'warn', 'error'],
                        help='Set the logging level')
    parser.add_argument("--api-key", type=str, help="YouTube Data API key")
    parser.add_argument("--db-file", type=str, help="database filename")
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
    api_key = args.api_key if args.api_key else os.getenv("API_KEY")
    db_file = args.db_file if args.db_file else os.getenv("DB_FILE")

    # set up logging
    logger = Logger(log_level)
    log = logger.get_logger()

    # pull metadata and comments from specified youtube video
    youtube = YouTubeDataAPI(logger, api_key)
    video_data = youtube.get_video_metadata(video_id)
    comments_df = youtube.get_comments(video_data)

    sa = SentimentAnalysis(logger)
    sa.add_sentiment_to_dataframe(comments_df)

    # Commit dataframe to database
    db = AstroDB(logger, db_file)
    db.insert_comment_dataframe(video_data, comments_df)

    log.debug('Collected data preview: \n{}'.format(comments_df))


if __name__ == "__main__":
    main()
