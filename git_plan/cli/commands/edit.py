"""Edit command

Author: Rory Byrne <rory@rory.bio>
"""
from typing import Any

from git_plan.cli.commands.command import Command
from git_plan.model.project import Project
from git_plan.service.plan import PlanService
from git_plan.service.ui import UIService


class Edit(Command):
    """Edit an existing commit"""

    subcommand = 'edit'

    def __init__(self, plan_service: PlanService, working_dir: str, ui_service: UIService):
        super().__init__()
        assert plan_service, "Plan service not injected"
        assert working_dir, "Working dir not injected"
        self._plan_service = plan_service
        self._ui_service = ui_service
        self._project = Project.from_working_dir(working_dir)

    def pre_command(self):
        """Perhaps some validation?"""
        pass

    def command(self):
        """Create a new commit"""
        commits = self._plan_service.get_commits(self._project)
        if not commits:
            print("No commits to edit.")
            return

        chosen_commit = self._ui_service.choose_commit(commits)

        self._plan_service.edit_commit(chosen_commit)

    def register_subparser(self, subparsers: Any):
        subparsers.add_parser(Edit.subcommand, help='Edit an existing commit plan.')