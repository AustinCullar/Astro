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

    def __init__(self, task_str: str, steps: int, console=None) -> None:
        self.task_str = task_str
        self.total_steps = steps

        super().__init__(
            TextColumn("{task.description} [progress.percentage]{task.percentage:>3.0f}%"),
            BarColumn(),
            MofNCompleteColumn(),
            TextColumn("•", style=console.get_style('log.message')),
            TimeElapsedColumn(),
            TextColumn("•", style=console.get_style('log.message')),
            TimeRemainingColumn(),
            console=console)

        self.task = super().add_task(f"[{console.get_style('log.message')}]" + task_str, total=self.total_steps)

    def advance(self, steps: int) -> None:
        super().update(self.task, advance=steps)

    def complete(self) -> None:
        return super().update(self.task, completed=self.total_steps)

    def set_completed(self, completed: int) -> None:
        return super().update(self.task, completed=completed)
