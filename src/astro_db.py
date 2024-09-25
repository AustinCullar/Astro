"""
Program to build a database of youtube comments.

Usage: TBD
"""
import sqlite3
import os
import string
import random

import pandas as pd

from dotenv import load_dotenv


class AstroDB:
    conn = None
    cursor = None
    logger = None

    def __init__(self, logger, db_file: str):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.logger = logger.get_logger()

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

        # Generate random names until we get one that doesn't exist
        while True:
            id_string = ''.join(random.choices(string.ascii_uppercase, k=12))

            if not self.comment_table_exists(id_string):
                break
            else:
                self.logger.warn('Comment table name collision!')

        return id_string

    def create_database(self):
        """
        Create the main table, 'Videos', which will track every video on which
        data is collected. It will also point to a seperate table in which comment
        data is stored for that particular video id.
        """
        self.cursor.execute("CREATE TABLE IF NOT EXISTS Videos ( \
            id INTEGER PRIMARY KEY AUTOINCREMENT, \
            author TEXT, \
            video_id TEXT, \
            comment_table TEXT)")

        self.conn.commit()

    def create_comment_table_for_video(self, video_id: str) -> str:
        """
        Create a new comment table for a specific video id.
        """
        author = 'TDOO'
        table_name = self.create_unique_table_name()

        self.cursor.execute("INSERT INTO Videos (author, video_id, comment_table) \
            VALUES ('{}', '{}', '{}')".format(author, video_id, table_name))

        self.cursor.execute("CREATE TABLE {} ( \
            id INTEGER PRIMARY KEY AUTOINCREMENT, \
            user TEXT, \
            comment TEXT, \
            date TEXT, \
            PSentiment, \
            NSentiment)".format(table_name))

        self.conn.commit()

        self.logger.debug('Video table {} created for video id {}'.format(table_name, video_id))

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
            table = table[0]

        return table

    def insert_comment(self, video_id: str, user: str, comment: str, date: str):
        """
        Given a video ID along with basic comment data, commit the data to the
        appropriate comment table.
        """
        comment_table = self.get_comment_table_for(video_id)

        if comment_table:
            self.logger.debug('Video table for {} already existed'.format(video_id))
            self.cursor.execute("SELECT comment_table FROM Videos WHERE video_id='{}'".format(video_id))
            comment_table = self.cursor.fetchone()[0]
        else:
            self.logger.debug('Video table for {} did not exist'.format(video_id))
            comment_table = self.create_comment_table_for_video(video_id)

        # insert comment info into DB
        self.cursor.execute("INSERT INTO '{}' (user, comment, date) \
            VALUES ('{}', '{}', '{}')".format(comment_table, user, comment, date))

        self.conn.commit()

    def insert_comment_dataframe(self, video_id: str, dataframe: pd.DataFrame):
        """
        Given a video ID and a dataframe, commit the dataframe to the database.
        """
        comment_table = self.get_comment_table_for(video_id)
        if not comment_table:
            self.logger.debug('Video table for {} did not exist'.format(video_id))
            comment_table = self.create_comment_table_for_video(video_id)

        # eventually we should use 'append' here
        dataframe.to_sql(comment_table, self.conn, if_exists='replace')


"""
This code is used for debugging and will likely be removed once proper unit testing is added.

def main():
    load_dotenv()
    db = AstroDB(os.getenv("DB_FILE"))

    db.create_database()

    db.insert_comment('4M-FeqYmwdg', 'acullar', 'hello there', '4.22.2017') 

if __name__ == "__main__":
    main()
"""
