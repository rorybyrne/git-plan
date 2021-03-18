"""Plan command

@author Rory Byrne <rory@rory.bio>
"""
from typing import Any

from git_plan import __version__
from git_plan.cli.commands.command import Command
from git_plan.exceptions import CommandNotFound, GitPlanException
from git_plan.service.plan import PlanService


class Plan(Command):
    """Create or update a plan."""

    subcommand = 'plan'

    def __init__(self, plan_service: PlanService, **kwargs):
        super().__init__(**kwargs)
        assert plan_service, "Plan service not injected"
        self._plan_service = plan_service

    def command(self, *, version: bool = False, **kwargs):  # pylint: disable=arguments-differ
        """Plan a commit"""

        if version:
            print(__version__)
            return

        if not self._cli:
            raise GitPlanException("Couldn't access the CLI instance.")

        if self._plan_service.has_commits(self._project):
            try:
                self._cli.invoke('list', **kwargs)
            except CommandNotFound:
                self._ui.bold("Something went wrong. Please open a Github issue!")
        else:
            self._cli.invoke('add', **kwargs)

    def register_subparser(self, subparsers: Any):
        subparsers.add_parser(self.subcommand, help='Add a new commit, or view existing ones.')
