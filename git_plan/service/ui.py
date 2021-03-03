"""UI service

Author: Rory Byrne <rory@rory.bio>
"""
from typing import List

from rich import print

from git_plan.model.commit import Commit


class UIService:

    @staticmethod
    def choose_commit(tasks: List[Commit]):
        """Choose from a set of tasks"""
        return tasks[0]

    def render_commits(self, commits: List[Commit], headline_only=True):
        """Renders a list of commits in pretty print"""
        for idx, commit in enumerate(commits):
            self._render_commit(commit, str(idx + 1), headline_only)
            if idx < len(commits) - 1:
                print('')

    def _render_commit(self, commit: Commit, tag: str, headline_only):
        if headline_only:
            print(f'[bold][{tag}][/bold] {commit.message.headline}')
        else:
            print(f'[bold][[magenta]{tag}[/magenta]][/bold] on {commit.branch}\n')
            print(f'    {commit.message.headline}\n')
            print(f'    {commit.message.body}')

