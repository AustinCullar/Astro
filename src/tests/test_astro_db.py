import pytest
import os

from unittest.mock import MagicMock

# Astro modules
from src.astro_db import AstroDB

test_video_ids = ['e-qUSPnOlbb', 'whautOBEjLTM', 'Sc_GwhJVdhRY']


@pytest.fixture(scope='function', params=[True, False])
def mock_comment_table_exists(request):
    """
    Mock AstroDB.comment_table_exists to return True on every call. This
    is used to stress AstroDB.create_unique_table_name.
    """
    mock = AstroDB.comment_table_exists
    mock.execute = MagicMock(return_value=request.param)


@pytest.fixture(scope='class')
def astro_db(logger):
    test_db_file = 'test.db'
    db = AstroDB(logger, test_db_file)
    yield db
    os.remove(test_db_file)


class TestAstroDB:
    created_comment_tables = []

    def test_create_videos_table(self, astro_db):
        astro_db.create_videos_table()

        conn = astro_db.get_db_conn()
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Videos'")
        result = cursor.fetchone()

        assert result

    @pytest.mark.parametrize('video_id', test_video_ids)
    def test_create_comment_table_for_video(self, astro_db, video_id):
        conn = astro_db.get_db_conn()
        cursor = conn.cursor()

        # create entry in Videos table along with a new comment table for that video
        comment_table_name = astro_db.create_comment_table_for_video(video_id)

        # verify creation of entry in Videos and the new comment table
        cursor.execute(f"SELECT comment_table FROM Videos WHERE video_id='{video_id}'")
        comment_table_from_video = cursor.fetchone()

        assert comment_table_from_video
        assert comment_table_from_video[0] == comment_table_name

        self.created_comment_tables.append(comment_table_name)

    def test_comment_table_exists(self, astro_db):
        conn = astro_db.get_db_conn()
        cursor = conn.cursor()

        for comment_table in self.created_comment_tables:
            assert astro_db.comment_table_exists(comment_table)

        # get existing comment table from Videos table
        for table_name in self.created_comment_tables:
            cursor.execute(f"SELECT * FROM Videos WHERE comment_table='{table_name}'")
            row = cursor.fetchone()

            assert row

            comment_table = row[3]  # comment_table is the 4th column
            assert comment_table in self.created_comment_tables

    @pytest.mark.parametrize('comment_table_exists', [True, False])
    def test_create_unique_table_name(self, astro_db, comment_table_exists):
        # this method generates a random 12 character string of capital letters
        # the likelihood of collision is extremely low (1 in (26^12))
        # using the mock below to simulate a name collision to exercise error path
        mock = astro_db
        mock.comment_table_exists = MagicMock(return_value=comment_table_exists)
        name = astro_db.create_unique_table_name()

        if not comment_table_exists:  # we're expecting a normal run, unlikely to have a name collision
            # verify that the returned string is valid for sql table names
            assert name
            assert '-' not in name
            assert '_' not in name
        else:
            assert not name

    @pytest.mark.parametrize('video_id', test_video_ids)
    def test_get_comment_table_for(self, astro_db, video_id):
        # verify that AstroDB finds the comment table
        table_name = astro_db.get_comment_table_for(video_id)

        assert table_name

        # verify that the database agrees with AstroDB
        conn = astro_db.get_db_conn()
        cursor = conn.cursor()

        cursor.execute(f"SELECT comment_table FROM Videos WHERE video_id='{video_id}'")
        database_table = cursor.fetchone()

        assert database_table
        assert database_table[0] == table_name

    @pytest.mark.parametrize('video_id', test_video_ids)
    def test_insert_comment_dataframe(self, astro_db, video_id, comment_dataframe):
        astro_db.insert_comment_dataframe(video_id, comment_dataframe)

        conn = astro_db.get_db_conn()
        cursor = conn.cursor()

        # check database for dataframe content
        query = f"SELECT comment_table FROM Videos WHERE video_id='{video_id}'"
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