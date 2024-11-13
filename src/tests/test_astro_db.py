import pytest
import sqlite3
import os

from unittest.mock import MagicMock

# Astro modules
from src.astro_db import AstroDB
from src.dataframe import CommentDataFrame
from src.tests.test_objects import test_video_data
from src.tests.astro_mocks import MockSqlite3Connection


@pytest.fixture(scope='function')
def astro_db(logger):
    test_db_file = 'test.db'
    db = AstroDB(logger, test_db_file)
    yield db
    os.remove(test_db_file)


@pytest.fixture(scope='function')
def mock_sqlite3_connect():
    # save the original connect function
    sqlite3_connect_orig = sqlite3.connect

    # pass instance of our own MockSqlite3Connection class to MagicMock
    sqlite_connect_mock = MockSqlite3Connection()
    sqlite3.connect = MagicMock(return_value=sqlite_connect_mock)

    # yield the sqlite_connect_mock object so that the test function can
    # set the return value
    yield sqlite_connect_mock

    # restore the original connect function
    sqlite3.connect = sqlite3_connect_orig


@pytest.fixture(scope='function')
def database_fault(mock_sqlite3_connect, logger):
    """
    Force the database queries to return None
    """
    mock_sqlite3_connect.set_return_value(None)
    return AstroDB(logger, 'test2.db')


class TestAstroDB:
    created_comment_tables = []

    def __get_comment_table_for_video_data(self, conn, video_data):
        cursor = conn.cursor()

        cursor.execute(f"SELECT comment_table FROM Videos WHERE video_id='{video_data.video_id}'")
        comment_table = cursor.fetchone()[0]

        return comment_table

    def __get_table_row_count(self, conn, table_name):
        cursor = conn.cursor()

        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        row_count = cursor.fetchone()[0]

        return row_count

    def __insert_dataframe_exception(self, astro_db, comment_dataframe, video_data) -> bool:
        if video_data and video_data.video_id:
            return False

        # expect an exception
        with pytest.raises(ValueError) as exception:
            astro_db.insert_comment_dataframe(video_data, comment_dataframe)
            assert str(exception.value) == 'Invalid video id'

        return True

    def test_create_videos_table(self, astro_db):
        astro_db.create_videos_table()

        conn = astro_db.get_db_conn()
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Videos'")
        result = cursor.fetchone()

        assert result

    @pytest.mark.parametrize('video_data', test_video_data)
    def test_create_comment_table_for_video(self, astro_db, video_data):
        conn = astro_db.get_db_conn()
        cursor = conn.cursor()

        bad_input = not video_data or \
            not video_data.channel_id or \
            not video_data.video_id

        if bad_input:  # expect an exception
            with pytest.raises(ValueError) as exception:
                comment_table_name = astro_db._AstroDB__create_comment_table_for_video(video_data)
                assert str(exception.value) == 'Invalid video data'
        else:
            # create entry in Videos table along with a new comment table for that video
            comment_table_name = astro_db._AstroDB__create_comment_table_for_video(video_data)

            # verify creation of entry in Videos and the new comment table
            cursor.execute(f"SELECT * FROM Videos WHERE video_id='{video_data.video_id}'")
            video_table_data = cursor.fetchone()

            assert video_table_data
            assert video_table_data[1] == video_data.channel_title
            assert video_table_data[2] == video_data.channel_id
            assert video_table_data[3] == video_data.video_id
            assert video_table_data[4] == video_data.view_count
            assert video_table_data[5] == video_data.like_count
            assert video_table_data[6] == video_data.comment_count
            assert video_table_data[7] == video_data.filtered_comment_count
            assert video_table_data[8] == comment_table_name

            self.created_comment_tables.append(comment_table_name)

    @pytest.mark.parametrize('table_names', [
                            ['AAA', 'BAA'],
                            ['ABB', 'BBB'],
                            ['ZAA', 'ABA'],
                            ['ZZZ', ''],
                            [None, 'AAA']
                            ])
    def test_create_unique_table_name(self, logger, mock_sqlite3_connect, table_names):
        mock_sqlite3_connect.set_return_value(table_names[0])
        astro_db = AstroDB(logger, 'test2.db')

        if table_names[0] == 'ZZZ':
            with pytest.raises(StopIteration) as exception:
                name = astro_db._AstroDB__create_unique_table_name()
                assert str(exception.value) == 'Limit exceeded for number of comment tables in database'
        else:
            name = astro_db._AstroDB__create_unique_table_name()
            assert name == table_names[1]

    @pytest.mark.parametrize('video_data', test_video_data)
    def test_insert_comment_dataframe(self, astro_db, video_data, comment_dataframe):
        if not self.__insert_dataframe_exception(astro_db, comment_dataframe, video_data):
            astro_db.insert_comment_dataframe(video_data, comment_dataframe)

            conn = astro_db.get_db_conn()
            cursor = conn.cursor()

            # check database for dataframe content
            query = f"SELECT comment_table FROM Videos WHERE video_id='{video_data.video_id}'"
            cursor.execute(query)
            comment_table = cursor.fetchone()

            # there should only be one comment table
            assert len(comment_table) == 1

            comment_table = comment_table[0]

            # grab all rows from coment table
            query = f"SELECT * FROM {comment_table}"
            cursor.execute(query)
            comment_data = cursor.fetchall()

            # verify that the data in the table matches that in the dataframe
            for (db_row, (_, dataframe_row)) in zip(comment_data, comment_dataframe.iterrows()):
                assert db_row[0] == dataframe_row['comment_id']
                assert db_row[1] == dataframe_row['comment']
                assert db_row[2] == dataframe_row['user']
                assert db_row[3] == dataframe_row['date']
                assert db_row[4] == dataframe_row['visible']

    @pytest.mark.parametrize('video_data', [video_data for video_data in test_video_data if video_data])
    def test_get_video_data(self, astro_db, video_data):
        conn = astro_db.get_db_conn()
        cursor = conn.cursor()

        if not video_data.video_id:
            with pytest.raises(ValueError) as exception:
                db_video_data = astro_db.get_video_data(video_data.video_id)
                assert str(exception.value) == 'Invalid video id'
        else:
            astro_db._AstroDB__create_comment_table_for_video(video_data)
            db_video_data = astro_db.get_video_data(video_data.video_id)

            cursor.execute(f"SELECT * from Videos WHERE video_id='{video_data.video_id}'")
            db_entry = cursor.fetchone()

            assert db_entry
            assert db_entry[1] == db_video_data.channel_title
            assert db_entry[2] == db_video_data.channel_id
            assert db_entry[3] == db_video_data.video_id
            assert db_entry[4] == db_video_data.view_count
            assert db_entry[5] == db_video_data.like_count
            assert db_entry[6] == db_video_data.comment_count
            assert db_entry[7] == db_video_data.filtered_comment_count

    @pytest.mark.parametrize('video_data', [test_video_data[0]])
    def test_new_comment_detection(self, astro_db, comment_dataframe, video_data):
        conn = astro_db.get_db_conn()
        cursor = conn.cursor()

        # insert dataframe
        astro_db.insert_comment_dataframe(video_data, comment_dataframe)

        # get newly created comment table
        comment_table = self.__get_comment_table_for_video_data(conn, video_data)
        orig_comment_count = self.__get_table_row_count(conn, comment_table)

        # append 2 new dummy comments to dataframe
        comment_dataframe2 = CommentDataFrame()
        comment_dataframe2.add_comment('id1', 'comment1', 'test_user', '10.25.2024')
        comment_dataframe2.add_comment('id2', 'comment2', 'test_user', '10.26.2024')

        # insert dataframe
        astro_db.insert_comment_dataframe(video_data, comment_dataframe2)
        new_comment_count = self.__get_table_row_count(conn, comment_table)

        # verify new comments were added
        cursor.execute(f"SELECT comment_id FROM {comment_table} WHERE user='test_user'")
        comment_ids = cursor.fetchall()

        assert len(comment_ids) == 2  # make sure we added 2 new comments
        for (comment_id, (_, df_row)) in zip(comment_ids, comment_dataframe2.iterrows()):
            assert comment_id[0] == df_row['comment_id']

        assert new_comment_count == orig_comment_count+2

    @pytest.mark.parametrize('video_data', [test_video_data[0]])
    def test_nonvisible_comment_detection(self, astro_db, comment_dataframe, video_data):
        conn = astro_db.get_db_conn()
        cursor = conn.cursor()

        # insert dataframe
        astro_db.insert_comment_dataframe(video_data, comment_dataframe)

        # get newly created comment table
        comment_table = self.__get_comment_table_for_video_data(conn, video_data)
        assert comment_table

        # insert same dataframe, but with last row dropped
        dropped_comment_id = comment_dataframe.get_column_values(column='comment_id')[-1]
        comment_dataframe.drop(comment_dataframe.row_count()-1)
        astro_db.insert_comment_dataframe(video_data, comment_dataframe)

        # verify that the comment's visibility was changed in the table
        cursor.execute(f"SELECT comment_id FROM {comment_table} WHERE visible=FALSE")
        comment_id = cursor.fetchone()[0]

        assert comment_id == dropped_comment_id

    @pytest.mark.parametrize('video_data', test_video_data)
    def test_update_video_data(self, astro_db, comment_dataframe, video_data):
        conn = astro_db.get_db_conn()
        cursor = conn.cursor()

        if not self.__insert_dataframe_exception(astro_db, comment_dataframe, video_data):
            # insert comment dataframe to force Video table entry creation
            astro_db.insert_comment_dataframe(video_data, comment_dataframe)

            video_data.view_count = 1235813
            video_data.like_count = 1111111
            video_data.comment_count = 2222222
            video_data.filtered_comment_count = 3333333

            astro_db.update_video_data(video_data)

            cursor.execute(f"SELECT * FROM Videos WHERE video_id='{video_data.video_id}'")
            db_entry = cursor.fetchone()

            assert db_entry[4] == video_data.view_count
            assert db_entry[5] == video_data.like_count
            assert db_entry[6] == video_data.comment_count
            assert db_entry[7] == video_data.filtered_comment_count
