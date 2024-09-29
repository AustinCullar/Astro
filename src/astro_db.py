"""
Class for managing comment/video database.
"""
import sqlite3
import string
import random

import pandas as pd


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

    def comment_table_exists(self, table_name: str) -> bool:
        """
        Check the 'Videos' table for an entry containing the provided
        table name in the 'comment_table' column.
        """

        query = f"SELECT * FROM Videos WHERE comment_table='{table_name}'"
        self.cursor.execute(query)
        table_exists = self.cursor.fetchone()

        return bool(table_exists)

    def create_unique_table_name(self) -> str:
        """
        Create a random table name from uppercase letters.
        """
        attempts = 3  # 3 attempts to generate unique string
        id_string = ''

        # Generate random names until we get one that doesn't exist
        while attempts > 0:
            id_string = ''.join(random.choices(string.ascii_uppercase, k=12))

            if self.comment_table_exists(id_string):
                self.logger.warning('Comment table name collision!')
                attempts -= 1
            else:
                return id_string

        return ''

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
        author = 'TDOO'
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
        get_comment_table_for_video = \
            f"SELECT comment_table FROM Videos WHERE video_id='{video_id}'"

        self.cursor.execute(get_comment_table_for_video)

        table = self.cursor.fetchone()
        if table:
            return table[0]
        else:
            return ''

    def insert_comment_dataframe(self, video_data, dataframe: pd.DataFrame):
        """
        Given a video ID and a dataframe, commit the dataframe to the database.
        """
        comment_table = self.get_comment_table_for(video_data.video_id)
        if not comment_table:
            self.logger.debug('Comment table for video id {} did not exist'.format(video_data.video_id))
            comment_table = self.create_comment_table_for_video(video_data)

        # eventually we should use 'append' here
        dataframe.to_sql(comment_table, self.conn, if_exists='replace')
        self.conn.commit()
