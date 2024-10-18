"""
This file defines the project color themes for anything printed to the console.
"""
from rich.theme import Theme
from rich.console import Console
from rich_argparse import ArgumentDefaultsRichHelpFormatter


class AstroTheme:
    astro_theme: Theme
    astro_console: Console
    astro_text_color = 'sky_blue3'

    def __init__(self):
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

        self.astro_console = Console(theme=self.astro_theme)
        self.__set_argparse_theme()

    def __set_argparse_theme(self):
        """
        Set the theme of the argparse help menu.
        """
        ArgumentDefaultsRichHelpFormatter.styles['argparse.args'] = self.astro_text_color  # for positional-arguments
        ArgumentDefaultsRichHelpFormatter.styles['argparse.groups'] = self.astro_text_color  # for group names
        ArgumentDefaultsRichHelpFormatter.styles['argparse.help'] = self.astro_text_color  # for argument's help text
        ArgumentDefaultsRichHelpFormatter.styles['argparse.metavar'] = 'green'  # for metavariables
        ArgumentDefaultsRichHelpFormatter.styles['argparse.prog'] = 'green'  # for %(prog)s in the usage
        ArgumentDefaultsRichHelpFormatter.styles['argparse.syntax'] = 'bold'  # for highlights of back-tick quoted text
        ArgumentDefaultsRichHelpFormatter.styles['argparse.text'] = self.astro_text_color  # for descriptions
        ArgumentDefaultsRichHelpFormatter.styles['argparse.default'] = 'italic'  # for %(default)s in the help

    def get_style(self):
        return self.astro_text_color

    def get_theme(self):
        return self.astro_theme

    def get_console(self):
        return self.astro_console
