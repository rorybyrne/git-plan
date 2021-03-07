"""List command

@author Rory Byrne <rory@rory.bio>
"""
from argparse import ArgumentParser
from typing import Any

from git_plan.cli.commands.command import Command
from git_plan.model.project import Project
from git_plan.service.plan import PlanService
from git_plan.service.ui import UIService


class List(Command):
    """List commits."""

    subcommand = 'list'

    def __init__(self, plan_service: PlanService, ui_service: UIService, working_dir: str):
        super().__init__()
        assert plan_service, "Plan service not injected"
        assert working_dir, "Working dir not injected"
        self._plan_service = plan_service
        self._ui_service = ui_service
        self._project = Project.from_working_dir(working_dir)

    def pre_command(self):
        """Check whether a plan already exists?"""
        pass

    def command(self, short=False, **kwargs):
        """List the planned commits"""
        commits = self._plan_service.get_commits(self._project)
        if len(commits) == 0:
            print("No commit plans.")
            return

        commits = sorted(commits, key=lambda c: c.id)
        return self._ui_service.render_commits(commits, headline_only=short)

    def register_subparser(self, subparsers: Any):
        parser: ArgumentParser = subparsers.add_parser(List.subcommand, help='List existing commit plans.')
        parser.add_argument('--short', dest='short', action='store_true')
