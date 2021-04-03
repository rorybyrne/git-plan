"""Edit command

Author: Rory Byrne <rory@rory.bio>
"""
from typing import Any

from git_plan.cli.commands.command import Command
from git_plan.service.plan import PlanService
from git_plan.util.decorators import requires_initialized, requires_git_repository


@requires_initialized
@requires_git_repository
class Edit(Command):
    """Edit an existing commit"""

    subcommand = 'edit'

    def __init__(self, plan_service: PlanService, **kwargs):
        super().__init__(**kwargs)
        assert plan_service, "Plan service not injected"
        self._plan_service = plan_service

    def command(self, **kwargs):
        """Create a new commit"""
        commits = self._plan_service.get_commits(self._repository)
        if not commits:
            self._ui.bold('No commits to edit.')
            return

        chosen_commit = self._ui.choose_commit(commits, 'Which plan do you want to edit?')

        self._plan_service.edit_commit(chosen_commit)

    def register_subparser(self, subparsers: Any):
        subparsers.add_parser(Edit.subcommand, help='Edit an existing commit plan.')
