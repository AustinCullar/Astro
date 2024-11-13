"""
Class for managing comment/video database.
"""
import sqlite3

import pandas as pd
from src.dataframe import read_comments_sql
from src.data_collection.data_structures import VideoData


class AstroDB:
    conn = None
    cursor = None
    logger = None

    def __init__(self, logger, db_file: str):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.logger = logger
        self.create_videos_table()

        self.logger.debug('Initializing database...')

    def __merge_comment_data(self, comment_table: str, new_dataframe):
        """
        Merge new comment data with existing data in local database. This logic
        will detect hidden comments and update their visibility status and then
        append any new comments to the comment table.
        """
        # pull comments from local database
        db_dataframe = read_comments_sql(f'SELECT * FROM {comment_table}', self.conn)
        if db_dataframe is None:
            raise LookupError(f'Failed to pull data from comment table: {comment_table}')

        # identify new comments as those present in the new dataframe, but not in the database dataframe
        new_comments = new_dataframe.not_in(db_dataframe)

        # identify nonvisible comments as those present in the database dataframe, but not in the new dataframe
        nonvisible_comments = db_dataframe.not_in(new_dataframe)

        if nonvisible_comments:
            self.logger.debug(f'Identified {nonvisible_comments.row_count()} nonvisible comments')

            # get comment ids of nonvisible comments
            nonvisible_ids = nonvisible_comments.get_column_values('comment_id')

            # update visibility value in local database
            for nonvisible_id in nonvisible_ids:
                # update database entry to reflect visible status
                self.cursor.execute(f"UPDATE {comment_table} SET \
                        visible=FALSE WHERE comment_id='{nonvisible_id}'")

        # check for new comments returned by the API, append to local database
        if new_comments:
            self.logger.info(f'Appending {new_comments.row_count()} new comments to local database')
            new_comments.to_sql(comment_table, self.conn, if_exists='append')
        else:
            self.logger.info(f'No new comments detected; local database is current')

        self.conn.commit()

    def __get_next_table_name(self, last_table_name: str) -> str:
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

    def __create_unique_table_name(self) -> str:
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

        new_name = self.__get_next_table_name(last_table_name)

        self.logger.debug('unique table name: {}'.format(new_name))

        return new_name

    def __create_comment_table_for_video(self, video_data) -> str:
        """
        Create a new comment table for a specific video id.
        """
        self.logger.debug('Creating comment table for new video...')

        if not video_data or \
                not video_data.channel_id or \
                not video_data.video_id:
            raise ValueError('Invalid video data')

        if not video_data.channel_title:
            # Missing the channel title is not critical, but should be investigated
            self.logger.warning('Missing channel title')

        table_name = self.__create_unique_table_name()
        assert table_name, "Failed to create unique comment table in database"

        query = f"INSERT INTO Videos \
                (channel_title, channel_id, video_id, \
                views, likes, comment_count, filtered_comment_count, \
                comment_table) \
                VALUES ( \
                '{video_data.channel_title}', \
                '{video_data.channel_id}', \
                '{video_data.video_id}', \
                '{video_data.view_count}', \
                '{video_data.like_count}', \
                '{video_data.comment_count}', \
                '{video_data.filtered_comment_count}', \
                '{table_name}')"

        self.cursor.execute(query)

        self.cursor.execute("CREATE TABLE {} ( \
            id INTEGER PRIMARY KEY AUTOINCREMENT, \
            comment_id TEXT, \
            comment TEXT, \
            user TEXT, \
            date TEXT, \
            visible INT, \
            PSentiment, \
            NSentiment)".format(table_name))

        self.conn.commit()

        self.logger.debug(f'Video table {table_name} created for video id {video_data.video_id}')

        return table_name

    def __get_comment_table_for(self, video_id: str) -> str:
        """
        Given a video id, return the associated comment table, if any.
        """
        self.logger.debug(f'Searching for comment table for video ID: {video_id}')

        self.cursor.execute(f"SELECT comment_table FROM Videos WHERE video_id='{video_id}'")
        table = self.cursor.fetchone()

        if table:
            return table[0]
        else:
            return ''

    def __get_nonvisible_comments(self, old=None, new=None) -> pd.DataFrame:
        """
        Return a new dataframe containing only rows which are present in `old`
        but not in `new`. This is used to determine which comments stored in the
        local database were not returned in the latest API response, indicating
        that the comment is no longer visible.
        """
        return old[~old.comment_id.isin(new.comment_id)]

    def __get_new_comments(self, old=None, new=None) -> pd.DataFrame:
        """
        Return a new dataframe ontaining only rows with are present in `new`
        but not in `old`. This is used to determine which comments in the API
        response are not currently stored in the local database.
        """
        return new[~new.comment_id.isin(old.comment_id)]

    def get_db_conn(self):
        return self.conn

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
            views INT, \
            likes INT, \
            comment_count INT, \
            filtered_comment_count INT, \
            comment_table TEXT)")

        self.conn.commit()

    def insert_comment_dataframe(self, video_data, dataframe):
        """
        Given a video ID and a dataframe, commit the dataframe to the database.
        """
        self.logger.debug('Inserting new comment dataframe...')

        if not video_data or not video_data.video_id:
            raise ValueError('Invalid video data')

        if dataframe is None:
            raise ValueError('Cannot insert NULL dataframe')

        comment_table = self.__get_comment_table_for(video_data.video_id)
        if comment_table:
            self.logger.debug('Merging new comment data with local database...')
            return self.__merge_comment_data(comment_table, dataframe)
        else:
            self.logger.debug(f'Comment table for video id {video_data.video_id} did not exist - creating it now')
            comment_table = self.__create_comment_table_for_video(video_data)

        dataframe.to_sql(comment_table, self.conn, if_exists='replace')

        self.conn.commit()

    def get_video_data(self, video_id: str) -> VideoData:
        """
        Given a video ID, search the database for any existing records for this video.
        """
        self.logger.debug('Retrieving video metadata from local database...')

        if not video_id:
            raise ValueError('Invalid video id')

        self.cursor.execute(f"SELECT * FROM Videos WHERE video_id='{video_id}'")
        db_record = self.cursor.fetchone()

        if not db_record:
            self.logger.debug(f'Video record not found in database for id {video_id}')
            return None

        video_data = VideoData(
                channel_title=db_record[1],
                channel_id=db_record[2],
                video_id=db_record[3],
                view_count=db_record[4],
                like_count=db_record[5],
                comment_count=db_record[6],
                filtered_comment_count=db_record[7])

        return video_data

    def update_video_data(self, video_data):
        """
        Update the Videos table with the new metadata.
        """
        self.logger.debug('Updating video metadata...')

        self.cursor.execute(f"UPDATE Videos SET \
                comment_count={video_data.comment_count}, \
                filtered_comment_count={video_data.filtered_comment_count}, \
                likes={video_data.like_count}, \
                views={video_data.view_count} \
                WHERE video_id='{video_data.video_id}'")

        self.conn.commit()
