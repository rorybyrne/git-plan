"""Delete command

Author: Rory Byrne <rory@rory.bio>
"""
from typing import Any

from git_plan.cli.commands.command import Command
from git_plan.service.plan import PlanService
from git_plan.util.decorators import requires_initialized, requires_git_repository


@requires_initialized
@requires_git_repository
class Delete(Command):
    """Delete an existing commit"""

    subcommand = 'delete'

    def __init__(self, plan_service: PlanService, **kwargs):
        super().__init__(**kwargs)
        assert plan_service, "Plan service not injected"
        self._plan_service = plan_service

    def command(self, **kwargs):
        """Create a new commit"""
        commits = self._plan_service.get_commits(self._repository)
        if not commits:
            self._ui.bold('No commits found.')
            return

        chosen_commit = self._ui.choose_commit(commits, 'Which plan do you want to delete?')

        self._ui.bold(f'{chosen_commit.message.headline}\n')
        confirm_msg = 'Are you sure you want to delete this commit?'
        if not self._ui.confirm(confirm_msg):
            self._ui.bold("Stopped.")
            return

        self._plan_service.delete_commit(chosen_commit)
        self._ui.bold('Deleted.')

    def register_subparser(self, subparsers: Any):
        subparsers.add_parser(Delete.subcommand, help='Delete a planned commit.')
