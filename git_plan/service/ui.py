"""UI service

Author: Rory Byrne <rory@rory.bio>
"""

import datetime as dt
from typing import List

import humanize
import inquirer
from rich import print as rich_print

from git_plan.exceptions import GitPlanException
from git_plan.model.commit import Commit


class UIService:
    """Functionality for rendering in the terminal"""

    @staticmethod
    def choose_commit(commits: List[Commit], message: str):
        """Choose from a set of tasks"""
        if len(commits) == 0:
            raise RuntimeError("Cannot choose from an empty list of commits.")

        if len(commits) == 1:
            return commits[0]

        options = [
            inquirer.List(
                "commit", message=message, choices=[(c.message.headline, c) for c in commits if c.message is not None]
            )
        ]

        answer = inquirer.prompt(options)
        if answer is None:
            raise GitPlanException("Got no answer.")

        return answer["commit"]

    @staticmethod
    def confirm(message: str) -> bool:
        """Ask the user for confirmation"""
        key = "confirm"
        questions = [inquirer.Confirm(key, message=message)]

        answers = inquirer.prompt(questions)
        if answers is None:
            raise GitPlanException("Got no answer.")

        return answers[key]

    def bold(self, message: str):
        """Print a bolded message"""
        self.print(f"[bold]{message}[/bold]")

    @staticmethod
    def print(message: str):
        """Print a message to the terminal"""
        rich_print(message)

    def render_commits(self, commits: List[Commit], headline_only=True):
        """Renders a list of commits in pretty print"""
        for idx, commit in enumerate(commits):
            self._render_commit(commit, str(idx + 1), headline_only)
            if idx < len(commits) - 1:
                print("")

    def _render_commit(self, commit: Commit, tag: str, headline_only):
        if not commit.updated_at:
            raise ValueError("Invalid commit: no updated_at field found.")

        if not commit.message:
            raise GitPlanException("Commit has no message.")

        time_display = f"[dim]({humanize.naturaltime(dt.datetime.fromtimestamp(commit.updated_at))})[/dim]"
        if headline_only:
            self.print(f"[bold][{tag}][/bold] {commit.message.headline} {time_display}")
        else:
            self.print(f"[bold][[magenta]{tag}[/magenta]][/bold] on {commit.branch} {time_display}\n")
            self.print(f"    {commit.message.headline}\n")
            body_lines = commit.message.body.split("\n")
            for line in body_lines:
                self.print(f"    {line}")
