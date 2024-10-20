"""
This file contains functionality for logging.
"""
import logging

from rich.logging import RichHandler
from rich.console import Console
from rich.table import Table
from rich.theme import Theme
from contextlib import contextmanager

from src.progress import AstroProgress


class AstroLogger(logging.Logger):
    log_level_str: str
    log_level: int
    console: Console
    astro_text_color: str
    astro_theme: Theme
    progress: AstroProgress
    log_file: str
    console_handler: RichHandler
    file_handler: logging.FileHandler

    def astro_config(self, log_level_str: str, astro_theme, log_file='astro_log.txt'):
        """
        Custom logging config.
        """
        # set log level
        self.log_level_str = log_level_str
        self.log_level = self.get_log_level(log_level_str)
        self.setLevel(self.log_level)

        # set color theme
        self.astro_theme = astro_theme

        # create console using the asto theme
        self.console = self.astro_theme.get_console()

        # create log handlers
        self.log_file = log_file
        self.console_handler = RichHandler(rich_tracebacks=True, console=self.console)
        self.file_handler = logging.FileHandler(self.log_file)
        log_handlers = [self.console_handler, self.file_handler]

        # configure formatting for file handler
        file_formatter = logging.Formatter(
                '%(asctime)s:%(levelname)6s: %(filename)14s:%(lineno)-3d %(message)-60s',
                '%Y-%m-%d %H:%M:%S')

        self.file_handler.setFormatter(file_formatter)

        # configure logging
        logging.basicConfig(format='%(message)s',
                            level=self.log_level,
                            handlers=log_handlers)

        # suppress google logs
        self.__suppress_logs('google', logging.WARNING)

    def __suppress_logs(self, name, level):
        """
        Suppress logging of external modules.
        """
        # explicitly set google logging to WARNING
        for logger_name in logging.root.manager.loggerDict:
            if logger_name.startswith(name):
                logging.getLogger(logger_name).setLevel(level)

    def progress_bar(self, task_str: str, steps: int):
        """
        Display a progress bar on the console.
        """
        self.progress = AstroProgress(task_str, steps, console=self.console)
        return self.progress

    def get_log_level(self, log_level: str) -> int:
        """
        Convert string log level to numeric log level.
        """
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

    def __rich_table(self, title=''):
        """
        Create a rich.Table object using the default project theme/style.
        """
        text_color = self.astro_theme.get_style()
        table = Table(style=text_color,
                      border_style=text_color,
                      header_style=text_color,
                      row_styles=[text_color],
                      title=title)

        return table

    def print_video_data(self, video_data):
        """
        Print VideoData object.
        """
        if video_data is None:
            return

        exclude_fields = ['filtered_comment_count']

        for attr, value in video_data.__dict__.items():
            if attr not in exclude_fields:
                self.info(f'{attr:>20}: {str(value)}')

    def print_dataframe(self, df, title=''):
        """
        Print the provided dataframe in rich.Table format.
        """
        max_comment_len = 30
        max_rows = 20
        row_count = 0

        # ensure dataframe contains only string values
        df = df.astype(str)

        table = self.__rich_table(title)

        # add dataframe columns
        for col in df.columns:
            table.add_column(col)

        # add dataframe rows
        for row in df.values:
            comment_len = len(row[0])

            # limit comment preview to `max_comment_len` characters
            row[0] = row[0][:max_comment_len]
            if comment_len > max_comment_len:
                row[0] += '...'

            table.add_row(*row)

            # only print `max_rows` rows
            row_count += 1
            if row_count == max_rows:
                table.add_row('...')
                break

        self.console.print(table)

    @contextmanager
    def log_file_only(self):
        """
        Provides a context in which logging will only go to the log file.
        """
        # temporarily raise log level of console handler
        self.console_handler.setLevel(logging.CRITICAL)

        yield

        # restore original log level
        self.console_handler.setLevel(self.log_level)
