"""
Tests for the Logging class.
"""
import pytest
from src.tests.test_objects import test_video_data


class TestLogging:
    @pytest.mark.parametrize('level', ['debug', 'info', 'warn', 'error', 'asdf'])
    def test_get_log_level(self, logger, level):
        valid_levels = ['debug', 'info', 'warn', 'error']

        if level in valid_levels:
            log_level = logger.get_log_level(level)

            if level == 'debug':
                assert log_level == 10
            elif level == 'info':
                assert log_level == 20
            elif level == 'warn':
                assert log_level == 30
            elif level == 'error':
                assert log_level == 40

        else:  # should assert error if invalid log level specified
            with pytest.raises(ValueError) as exception:
                logger.get_log_level(level)

            assert str(exception.value) == "Invalid logger level specified: {}".format(level)

    @pytest.mark.parametrize('obj', test_video_data)
    @pytest.mark.parametrize('title', ['title1', 'title-2', 'title_3'])
    def test_print_object(self, logger, obj, title):
        logger.print_object(obj, title=title)

    @pytest.mark.parametrize('title', ['title1', 'title-2', 'title_3'])
    def test_print_dataframe(self, logger, comment_dataframe, title):
        logger.print_dataframe(comment_dataframe, title=title)
