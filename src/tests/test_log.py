"""
Tests for the Logging class.
"""
import pytest
import logging

# Astro modules
from src.log import AstroLogger


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
                logger.astro_config(level) # this will call get_log_level()

            assert str(exception.value) == "Invalid logger level specified: {}".format(level)

    @pytest.mark.parametrize('obj', [])
    @pytest.mark.parametrize('title', [])
    def test_print_object(self, logger, obj, title):
        pass

    @pytest.mark.parametrize('df', [])
    @pytest.mark.parametrize('title', [])
    def test_print_dataframe(self, logger, df, title):
        pass
