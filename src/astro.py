"""
Main entry point for Astro data collection. This program will
leverage the YouTube Data API to gather data from YouTube videos.
"""
import os
import argparse
import logging

from dotenv import load_dotenv
from data_collection.yt_data_api import YouTubeDataAPI
from data_collection.sentiment import SentimentAnalysis
from log import AstroLogger
from astro_db import AstroDB
from theme import AstroTheme
from rich_argparse import ArgumentDefaultsRichHelpFormatter


def extract_video_id_from_url(url: str) -> str:
    """
    Grab the video ID from the provided URL. The ID will come after
    the substring 'v=' in the URL, so I just split the string on that
    substring and return the latter half.
    """

    video_id = url.split('v=')[1]
    if not YouTubeDataAPI.valid_video_id(video_id):
        raise ValueError('Invalid video URL provided')

    return video_id


def parse_args(astro_theme):
    """
    Argument parsing logic. Returns the arguments parsed from the CLI
    """
    description = "A tool for YouTube data collection."

    parser = argparse.ArgumentParser(description=description,
                                     formatter_class=ArgumentDefaultsRichHelpFormatter)

    parser.add_argument("youtube_url", type=str, help="youtube video URL")
    parser.add_argument("-l", "--log", type=str, choices=['debug', 'info', 'warn', 'error'],
                        help='Set the logging level', default='info')
    parser.add_argument("--api-key", type=str, help="YouTube Data API key")
    parser.add_argument("--db-file", type=str, help="database filename", default='astro.db')
    args = parser.parse_args()

    return args


def main():
    # load astro color scheme
    astro_theme = AstroTheme()

    # parse arguments
    args = parse_args(astro_theme)
    video_id = extract_video_id_from_url(args.youtube_url)

    # load environment variables
    load_dotenv()

    # prioritize log level provided on CLI, fallback to env variable
    log_level = args.log if args.log else os.getenv("LOG_LEVEL")
    api_key = args.api_key if args.api_key else os.getenv("API_KEY")
    db_file = args.db_file if args.db_file else os.getenv("DB_FILE")

    # set up logging
    logging.setLoggerClass(AstroLogger)
    logger = logging.getLogger(__name__)
    logger.astro_config(log_level, astro_theme)

    logger.info('Collecting video data...')

    # collect metadata for provided video
    youtube = YouTubeDataAPI(logger, api_key)
    video_data = youtube.get_video_metadata(video_id)

    logger.print_object(video_data, title="Video data")

    # check local database for existing data on provided video
    db = AstroDB(logger, db_file)
    db_video_data = db.get_video_data(video_data.video_id)

    if db_video_data:  # we already have a database table for this video
        # determine how many new comments we need to fetch
        video_data.comment_count -= db_video_data.comment_count

        if 0 >= video_data.comment_count:
            logger.info('Comment data is current; no new comments to collect')
            # if comments have been deleted, video_data.comment_count may be a negative value
            # explicitly set comment_count to 0 here to avoid adding negative value to db
            video_data.comment_count = 0
            db.update_video_data(video_data)
            return

    if video_data.comments_disabled:
        logger.info('Comments have been disabled for the provided video')
        db.update_video_data(video_data)
        return

    # collect comments from the provided video
    comments_df = youtube.get_comments(video_data)

    # update the video data in the local database
    db.update_video_data(video_data)

    # gather sentiment data on the comments, adding data to the dataframe
    sa = SentimentAnalysis(logger)
    sa.add_sentiment_to_dataframe(comments_df)

    # commit dataframe to database
    db.insert_comment_dataframe(video_data, comments_df)

    # print filtered comment information
    db_video_data = db.get_video_data(video_data.video_id)
    logger.info('Video has filtered ' +
                f'{db_video_data.filtered_comment_count/db_video_data.comment_count*100:.2f}% ' +
                'of comments')

    logger.print_dataframe(comments_df, title='Comment data preview')

    logger.info('Data collection complete.')


if __name__ == "__main__":
    main()
