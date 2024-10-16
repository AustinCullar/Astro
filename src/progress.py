"""
Progress bar utilities.
"""
from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)


class AstroProgress(Progress):
    total_steps: int
    task: int

    def __init__(self, task_str: str, steps: int, console=None, style=None):
        self.task_str = task_str
        self.total_steps = steps

        super().__init__(
            TextColumn("{task.description} [progress.percentage]{task.percentage:>3.0f}%"),
            BarColumn(),
            MofNCompleteColumn(),
            TextColumn("•", style=style),
            TimeElapsedColumn(),
            TextColumn("•", style=style),
            TimeRemainingColumn(),
            console=console)

        self.task = super().add_task(f'[{style}]' + task_str, total=self.total_steps)

    def advance(self, steps: int):
        super().update(self.task, advance=steps)

    def complete(self):
        return super().update(self.task, completed=self.total_steps)
