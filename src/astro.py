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


def parse_args(astro_theme):
    """
    Argument parsing logic. Returns the arguments parsed from the CLI
    """
    description = "A tool for YouTube data collection."

    parser = argparse.ArgumentParser(description=description,
                                     formatter_class=ArgumentDefaultsRichHelpFormatter)

    parser.add_argument('youtube_url', type=str, help='youtube video URL')
    parser.add_argument('-l', '--log', type=str, choices=['debug', 'info', 'warn', 'error'],
                        help='Set the logging level', default='info')
    parser.add_argument('--api-key', type=str, help='YouTube Data API key')
    parser.add_argument('--db-file', type=str, help='database filename', default='astro.db')
    parser.add_argument('--log-file', type=str, help='log output to specified file', default='astro_log.txt')
    parser.add_argument('-j', '--log-json', type=bool, help='log json API responses',
                        default=False, action=argparse.BooleanOptionalAction)
    args = parser.parse_args()

    return args


def main():
    # load astro color scheme
    astro_theme = AstroTheme()

    # parse arguments
    args = parse_args(astro_theme)

    # load environment variables
    load_dotenv()

    # prioritize log level provided on CLI, fallback to env variable
    log_level = args.log if args.log else os.getenv("LOG_LEVEL")
    api_key = args.api_key if args.api_key else os.getenv("API_KEY")
    db_file = args.db_file if args.db_file else os.getenv("DB_FILE")
    log_file = args.log_file if args.log_file else os.getenv("LOG_FILE")
    log_json = args.log_json if args.log_json else os.getenv("LOG_JSON")

    # set up logging
    logging.setLoggerClass(AstroLogger)
    logger = logging.getLogger(__name__)
    logger.astro_config(log_level, astro_theme, log_file=log_file)

    # collect metadata for provided video
    youtube = YouTubeDataAPI(logger, api_key, log_json)
    video_data = youtube.get_video_metadata(args.youtube_url)

    logger.print_video_data(video_data)

    # connect to local database
    db = AstroDB(logger, db_file)

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
