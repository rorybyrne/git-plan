"""Commit command

Author: Rory Byrne <rory@rory.bio>
"""
from typing import Any

from git_plan.cli.commands.command import Command
from git_plan.exceptions import CommitAbandoned
from git_plan.service.git import GitService
from git_plan.service.plan import PlanService
from git_plan.util.decorators import requires_initialized, requires_git_repository


@requires_initialized
@requires_git_repository
class Commit(Command):
    """Commit a plan"""

    subcommand = 'commit'

    def __init__(self, plan_service: PlanService, git_service: GitService, **kwargs):
        super().__init__(**kwargs)
        assert plan_service, "Plan service not injected"
        assert git_service, "Git service not injected"
        self._plan_service = plan_service
        self._git_service = git_service

    def command(self, **kwargs):
        """Create a new commit"""
        plans = self._plan_service.get_plans(self._repository)
        if not plans:
            print("No plans found.")
            return

        if not self._git_service.has_staged_files():
            print("No staged files.")
            return

        chosen_plan = self._ui.choose_plan(plans, 'Which plan do you want to commit?')
        try:
            self._git_service.commit(chosen_plan)
            self._plan_service.delete_plan(chosen_plan)
        except CommitAbandoned:
            print("Commit abandoned.")

    def register_subparser(self, subparsers: Any):
        subparsers.add_parser(Commit.subcommand, help='Commit a plan.')
