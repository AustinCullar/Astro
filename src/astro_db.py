"""
Class for managing comment/video database.
"""
import sqlite3
import string

import pandas as pd
from src.data_collection.yt_data_api import YouTubeDataAPI

class AstroDB:
    conn = None
    cursor = None
    logger = None

    def __init__(self, logger, db_file: str):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.logger = logger.get_logger()
        self.create_videos_table()

    def get_db_conn(self):
        return self.conn

    def get_next_table_name(self, last_table_name: str) -> str:
        """
        Roll the provided string forward by 'incrementing' the
        letters. See below for some example transitions:

        AAA -> BAA
        BAA -> CAA
        ...
        ZAA -> ABA
        ABA -> BBA
        """
        # 'roll' the name forward
        def next_char(c: chr) -> chr:
            return chr(ord(c) + 1)

        new_name = ''
        rolled = 0

        for i in range(len(last_table_name)):
            if last_table_name[i] != 'Z':
                new_name += next_char(last_table_name[i])
                new_name += last_table_name[i+1:len(last_table_name)]
                break
            else:
                rolled += 1
                new_name += 'A'
                if rolled == len(last_table_name):
                    raise StopIteration("Limit exceeded for number of comment tables in database")

        return new_name

    def create_unique_table_name(self) -> str:
        """
        This function effectively implements a string odometer. The
        name returned will be a 3 character string consisting of capital
        letters. Each successive call will 'roll forward' the last-created
        comment table name.

        Once the odometer reaches its limit of ZZZ, the next call will
        result in an exception. This should only happen after the creation of
        26^3 (17576) tables, which is a limit I'm comfortable with since I doubt
        we'll be tracking over one hundred YouTube videos, let alone over 17k.
        """
        # Get most recent comment table name by grabbing latest entry in the Videos table
        self.cursor.execute("SELECT comment_table FROM Videos ORDER BY id DESC LIMIT 1")

        last_table_name = self.cursor.fetchone()
        if not last_table_name:  # this is the first comment table we're creating
            return 'AAA'
        else:
            last_table_name = last_table_name[0]

        self.logger.debug('last table name: {}'.format(last_table_name))

        new_name = self.get_next_table_name(last_table_name)

        self.logger.debug('unique table name: {}'.format(new_name))

        return new_name

    def create_videos_table(self):
        """
        Create the main table, 'Videos', which will track every video on which
        data is collected. It will also point to a seperate table in which comment
        data is stored for that particular video id.
        """
        self.cursor.execute("CREATE TABLE IF NOT EXISTS Videos ( \
            id INTEGER PRIMARY KEY AUTOINCREMENT, \
            channel_title TEXT, \
            channel_id TEXT, \
            video_id TEXT, \
            comment_table TEXT)")

        self.conn.commit()

    def create_comment_table_for_video(self, video_data) -> str:
        """
        Create a new comment table for a specific video id.
        """
        if not video_data:
            raise ValueError('NULL video data')

        if not video_data.channel_id or not YouTubeDataAPI.valid_video_id(video_data.video_id):
            raise ValueError('Invalid video data')

        if not video_data.channel_title:
            # Missing the channel title is not critical, but should be investigated
            self.logger.warn('Missing channel title')

        table_name = self.create_unique_table_name()
        assert table_name, "Failed to create unique comment table in database"

        query = f"INSERT INTO Videos (channel_title, channel_id, video_id, comment_table) \
                VALUES ( \
                '{video_data.channel_title}', \
                '{video_data.channel_id}', \
                '{video_data.video_id}', \
                '{table_name}')"

        self.cursor.execute(query)

        self.cursor.execute("CREATE TABLE {} ( \
            id INTEGER PRIMARY KEY AUTOINCREMENT, \
            user TEXT, \
            comment TEXT, \
            date TEXT, \
            PSentiment, \
            NSentiment)".format(table_name))

        self.conn.commit()

        self.logger.debug('Video table {} created for video id {}'.format(table_name, video_data.video_id))

        return table_name

    def get_comment_table_for(self, video_id: str) -> str:
        """
        Given a video id, return the associated comment table, if any.
        """
        if not YouTubeDataAPI.valid_video_id(video_id):  # don't waste time querying database
            return ''

        get_comment_table_for_video_id = \
            f"SELECT comment_table FROM Videos WHERE video_id='{video_id}'"

        self.cursor.execute(get_comment_table_for_video_id)

        table = self.cursor.fetchone()

        if table:
            return table[0]
        else:
            return ''

    def insert_comment_dataframe(self, video_data, dataframe: pd.DataFrame):
        """
        Given a video ID and a dataframe, commit the dataframe to the database.
        """
        if not video_data:
            raise ValueError('NULL video data')

        if not YouTubeDataAPI.valid_video_id(video_data.video_id):
            raise ValueError('Invalid video id')

        comment_table = self.get_comment_table_for(video_data.video_id)
        if not comment_table:
            self.logger.debug('Comment table for video id {} did not exist'.format(video_data.video_id))
            comment_table = self.create_comment_table_for_video(video_data)

        # eventually we should use 'append' here
        dataframe.to_sql(comment_table, self.conn, if_exists='replace')
        self.conn.commit()
