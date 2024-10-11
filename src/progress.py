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

    def __init__(self, task_str: str, steps: int):
        self.task_str = task_str
        self.total_steps = steps

        super().__init__(
            TextColumn("{task.description} [progress.percentage]{task.percentage:>3.0f}%"),
            BarColumn(),
            MofNCompleteColumn(),
            TextColumn("•"),
            TimeElapsedColumn(),
            TextColumn("•"),
            TimeRemainingColumn())

        self.task = super().add_task('[green]' + task_str, total=self.total_steps)

    def advance(self, steps: int):
        super().update(self.task, advance=steps)

    def complete(self):
        return super().update(self.task, completed=self.total_steps)
