"""Plan command

@author Rory Byrne <rory@rory.bio>
"""
from typing import Any

from git_plan import __version__
from git_plan.cli.commands.command import Command
from git_plan.exceptions import CommandNotFound
from git_plan.service.plan import PlanService
from git_plan.util.decorators import requires_initialized
from git_plan.util.version import get_version_from_repo


@requires_initialized
class Plan(Command):
    """Create or update a plan."""

    subcommand = 'plan'

    def __init__(self, plan_service: PlanService, **kwargs):
        super().__init__(**kwargs)
        assert plan_service, "Plan service not injected"
        self._plan_service = plan_service

    def pre_command(self):
        """Check whether a plan already exists?"""
        pass

    def command(self, version=False, **kwargs):
        """Plan a commit"""

        if version:
            print(__version__)
            return 0

        if self._plan_service.has_commits(self._project):
            try:
                return self._cli.invoke('list', **kwargs)
            except CommandNotFound as e:
                self._ui.bold("Something went wrong. Please open a Github issue!")
        else:
            self._cli.invoke('add', **kwargs)

    def register_subparser(self, subparsers: Any):
        subparsers.add_parser(Plan.subcommand, help='Add a new commit, or view existing ones.')
