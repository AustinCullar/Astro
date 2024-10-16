"""
This file contains functionality for logging.
"""
import logging

from rich.logging import RichHandler
from rich.console import Console
from rich.table import Table
from rich.theme import Theme
from rich import print as rprint

from src.progress import AstroProgress


class AstroLogger(logging.Logger):
    log_level_str: str
    log_level: int
    console: Console
    astro_text_color: str
    astro_theme: Theme
    progress: AstroProgress

    def astro_config(self, log_level_str: str):
        """
        Custom logging config.
        """
        self.log_level_str = log_level_str
        self.log_level = self.get_log_level(log_level_str)

        self.setLevel(self.log_level)

        # define astro color theme
        self.astro_text_color = 'sky_blue3'
        self.astro_theme = Theme({
            "log.message": self.astro_text_color,
            "logging.level.info": 'blue_violet',
            "logging.level.warning": "orange_red1",
            "logging.level.error": "red",
            "bar.finished": "green",
            "progress.elapsed": self.astro_text_color,
            "progress.remaining": self.astro_text_color,
            "progress.percentage": "green",
            "table.title": "bold " + self.astro_text_color})

        # create console using the asto theme
        self.console = Console(theme=self.astro_theme)

        # configure logging
        logging.basicConfig(format='%(message)s',
                            level=self.log_level,
                            handlers=[RichHandler(rich_tracebacks=True,
                                                  console=self.console)])

        # suppress google logs
        self.suppress_logs('google', logging.WARNING)

    def suppress_logs(self, name, level):
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
        self.progress = AstroProgress(task_str, steps, console=self.console, style=self.astro_text_color)
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

    def rich_table(self, title=''):
        """
        Create a rich.Table object using the default project theme/style.
        """
        table = Table(style=self.astro_text_color,
                      border_style=self.astro_text_color,
                      header_style=self.astro_text_color,
                      row_styles=[self.astro_text_color],
                      title=title)

        return table

    def print_object(self, obj, title=''):
        """
        Print the attributes of the provided object. Useful for debugging.
        """
        if obj is None:
            return

        # only print objects in debug or info mode
        if self.log_level > logging.INFO:
            return

        table = self.rich_table(title)
        table.add_column("Attribute")
        table.add_column("Value")

        for attr, value in obj.__dict__.items():
            table.add_row(attr, str(value))

        self.console.print(table)

    def print_dataframe(self, df, title=''):
        """
        Print the provided dataframe in rich.Table format.
        """
        max_comment_len = 30
        max_rows = 20
        row_count = 0

        # ensure dataframe contains only string values
        df = df.astype(str)

        table = self.rich_table(title)

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

    def print_json(self, json_obj):
        """
        Easy way to print properly formatted json.
        """
        rprint(json_obj)
