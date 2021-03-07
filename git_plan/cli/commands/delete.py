"""Delete command

Author: Rory Byrne <rory@rory.bio>
"""
from typing import Any

from git_plan.cli.commands.command import Command
from git_plan.service.plan import PlanService
from git_plan.service.ui import UIService
from git_plan.util.decorators import requires_initialized


@requires_initialized
class Delete(Command):
    """Delete an existing commit"""

    subcommand = 'delete'

    def __init__(self, plan_service: PlanService, ui_service: UIService, **kwargs):
        super().__init__(**kwargs)
        assert plan_service, "Plan service not injected"
        self._plan_service = plan_service
        self._ui_service = ui_service

    def pre_command(self):
        """Perhaps some validation?"""
        pass

    def command(self, **kwargs):
        """Create a new commit"""
        commits = self._plan_service.get_commits(self._project)
        if not commits:
            print("No commits found.")
            return

        chosen_commit = self._ui_service.choose_commit(commits, 'Which plan do you want to delete?')

        self._ui_service.bold(f'{chosen_commit.message.headline}\n')
        confirm_msg = f'Are you sure you want to delete this commit?'
        if not self._ui_service.confirm(confirm_msg):
            print("Stopped.")
            return

        self._plan_service.delete_commit(chosen_commit)
        print('Deleted.')

    def register_subparser(self, subparsers: Any):
        subparsers.add_parser(Delete.subcommand, help='Delete a planned commit.')
