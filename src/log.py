"""
This file contains functionality for logging.
"""
import logging


class Logger:
    log_level_str: str
    log_level: int
    logger: logging.Logger

    def __init__(self, log_level_str: str):
        self.log_level_str = log_level_str
        self.log_level = self.get_log_level(log_level_str)
        self.logger = self.initialize_logging()

    def get_log_level(self, log_level: str) -> int:
        if log_level == "debug":
            log_level = logging.DEBUG
        elif log_level == "info":
            log_level = logging.INFO
        elif log_level == "warn":
            log_level = logging.WARNING
        elif log_level == 'error':
            log_level = logging.ERROR
        else:
            raise ValueError("Invalid logger level specified: {}".format(log_level))

        return log_level

    def initialize_logging(self) -> logging.Logger:
        logger = logging.getLogger(__name__)
        logging.basicConfig(format='%(levelname)s:%(filename)s:%(funcName)s: %(message)s', level=self.log_level)

        return logger

    def get_logger(self) -> logging.Logger:
        return self.logger

    def level(self, log_level_str: str) -> bool:
        return self.get_log_level(log_level_str) == self.log_level
