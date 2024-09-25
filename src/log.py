"""
This file contains functionality for logging.
"""
import logging


class Logger:

    def __init__(self, log_level_str: str):
        self.log_level = self.get_log_level(log_level_str)
        self.logger = self.initialize_logging()

    def get_log_level(self, log_level: str) -> int:
        log_level = log_level.upper()

        if log_level == "DEBUG":
            log_level = logging.DEBUG
        elif log_level == "INFO":
            log_level = logging.INFO
        elif log_level == "WARNING":
            log_level = logging.WARNING
        else:
            log_level = logging.ERROR

        return log_level

    def initialize_logging(self) -> logging.Logger:
        logger = logging.getLogger(__name__)
        logging.basicConfig(format='%(levelname)s:%(filename)s:%(funcName)s: %(message)s', level=self.log_level)

        return logger

    def get_logger(self) -> logging.Logger:
        return self.logger
