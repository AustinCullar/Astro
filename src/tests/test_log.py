"""
Tests for the Logging class.
"""
import pytest

# Astro modules
from src.log import Logger


class TestLogging:
    @pytest.mark.parametrize('level', ['debug', 'info', 'warn', 'error', 'asdf'])
    def test_get_log_level(self, level):
        valid_levels = ['debug', 'info', 'warn', 'error']

        if level in valid_levels:
            logger = Logger(level)
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
                logger = Logger(level)  # this will call get_log_level()

            assert str(exception.value) == "Invalid logger level specified: {}".format(level)
