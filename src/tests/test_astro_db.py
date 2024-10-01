import pytest
import sqlite3
import os

from unittest.mock import MagicMock

# Astro modules
from src.astro_db import AstroDB
from src.data_collection.data_structures import VideoData
from src.tests.astro_mocks import MockSqlite3Connection

test_video_data = [VideoData(video_id='e-qUSPnOlbb',
                             channel_id='itXtJBHdZchKKjlnVrjXeCln',
                             channel_title='YouTube_User1',
                             view_count=0,
                             like_count=0,
                             comment_count=0),
                   VideoData(video_id='whautOBEjLTM',
                             channel_id='FvlvKP-khoFMOeyBzmXuaazd',
                             channel_title='TestUser',
                             view_count=775,
                             like_count=212,
                             comment_count=0),
                   VideoData(video_id='Sc_GwhJVdhRY',
                             channel_id='LTO_OySEsmnRtoK-bkAeWXjW',
                             channel_title='User_YT99',
                             view_count=12345,
                             like_count=66423,
                             comment_count=76123)]


@pytest.fixture(scope='class')
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


class TestAstroDB:
    created_comment_tables = []

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

        # create entry in Videos table along with a new comment table for that video
        comment_table_name = astro_db.create_comment_table_for_video(video_data)

        # verify creation of entry in Videos and the new comment table
        cursor.execute(f"SELECT * FROM Videos WHERE video_id='{video_data.video_id}'")
        video_table_data = cursor.fetchone()

        assert video_table_data
        assert video_table_data[1] == video_data.channel_title
        assert video_table_data[2] == video_data.channel_id
        assert video_table_data[3] == video_data.video_id
        assert video_table_data[4] == comment_table_name

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
                name = astro_db.create_unique_table_name()
                assert str(exception.value) == "Limit exceeded for number of comment tables in database"
        else:
            name = astro_db.create_unique_table_name()
            assert name == table_names[1]


    @pytest.mark.parametrize('video_data', test_video_data)
    def test_get_comment_table_for(self, astro_db, video_data):
        # verify that AstroDB finds the comment table
        table_name = astro_db.get_comment_table_for(video_data.video_id)

        assert table_name

        # verify that the database agrees with AstroDB
        conn = astro_db.get_db_conn()
        cursor = conn.cursor()

        cursor.execute(f"SELECT comment_table FROM Videos WHERE video_id='{video_data.video_id}'")
        database_table = cursor.fetchone()

        assert database_table
        assert database_table[0] == table_name

    @pytest.mark.parametrize('video_data', test_video_data)
    def test_insert_comment_dataframe(self, astro_db, video_data, comment_dataframe):
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

        # grab all rows from coment tables
        query = f"SELECT * FROM {comment_table}"
        cursor.execute(query)
        comment_data = cursor.fetchall()

        # verify that the data in the table matches that in the dataframe
        index = 0
        for row in comment_data:
            assert row[0] == index
            assert row[1] == comment_dataframe.loc[index]['comment']
            assert row[2] == comment_dataframe.loc[index]['user']
            assert row[3] == comment_dataframe.loc[index]['date']

            index += 1
