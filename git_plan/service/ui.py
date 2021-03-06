"""UI service

Author: Rory Byrne <rory@rory.bio>
"""
from typing import List

import inquirer
from rich import print

from git_plan.model.commit import Commit


class UIService:

    @staticmethod
    def choose_commit(commits: List[Commit], message: str):
        """Choose from a set of tasks"""
        if len(commits) == 0:
            raise RuntimeError("Cannot choose from an empty list of commits.")
        elif len(commits) == 1:
            return commits[0]

        options = [
            inquirer.List(
                'commit',
                message=message,
                choices=[(c.message.headline, c) for c in commits]
            )
        ]

        answer = inquirer.prompt(options)

        return answer['commit']

    @staticmethod
    def confirm(message: str) -> bool:
        key = 'confirm'
        questions = [inquirer.Confirm(key, message=message)]

        answers = inquirer.prompt(questions)

        return answers[key]

    @staticmethod
    def bold(message: str):
        print(f'[bold]{message}[/bold]')

    def render_commits(self, commits: List[Commit], headline_only=True):
        """Renders a list of commits in pretty print"""
        for idx, commit in enumerate(commits):
            self._render_commit(commit, str(idx + 1), headline_only)
            if idx < len(commits) - 1:
                print('')

    @staticmethod
    def _render_commit(commit: Commit, tag: str, headline_only):
        if headline_only:
            print(f'[bold][{tag}][/bold] {commit.message.headline}')
        else:
            print(f'[bold][[magenta]{tag}[/magenta]][/bold] on {commit.branch}\n')
            print(f'    {commit.message.headline}\n')
            body_lines = commit.message.body.split('\n')
            for line in body_lines:
                print(f'    {line}')
