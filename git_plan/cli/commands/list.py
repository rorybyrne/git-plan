"""List command

@author Rory Byrne <rory@rory.bio>
"""
from argparse import ArgumentParser
from typing import Any

from git_plan.cli.commands.command import Command
from git_plan.service.plan import PlanService
from git_plan.service.ui import UIService
from git_plan.util.decorators import requires_initialized


@requires_initialized
class List(Command):
    """List commits."""

    subcommand = 'list'

    def __init__(self, plan_service: PlanService, ui_service: UIService, **kwargs):
        super().__init__(**kwargs)
        assert plan_service, "Plan service not injected"
        self._plan_service = plan_service
        self._ui = ui_service

    def pre_command(self):
        """Check whether a plan already exists?"""
        pass

    def command(self, long=False, **kwargs):
        """List the planned commits"""
        commits = self._plan_service.get_commits(self._project)
        if len(commits) == 0:
            self._ui.bold("No commit plans.")
            return

        commits = sorted(commits, key=lambda c: c.id)
        return self._ui.render_commits(commits, headline_only=not long)

    def register_subparser(self, subparsers: Any):
        parser: ArgumentParser = subparsers.add_parser(List.subcommand, help='List existing commit plans.')
        parser.add_argument('--long', dest='long', action='store_true')
