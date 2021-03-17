"""Add command

@author Rory Byrne <rory@rory.bio>
"""
from typing import Any

from git_plan.cli.commands.command import Command
from git_plan.exceptions import PlanEmpty
from git_plan.service.plan import PlanService
from git_plan.util.decorators import requires_initialized


@requires_initialized
class Add(Command):
    """Add a new commit"""

    subcommand = 'add'

    def __init__(self, plan_service: PlanService, **kwargs):
        super().__init__(**kwargs)
        assert plan_service, "Plan service not injected"
        self._plan_service = plan_service

    def command(self, **kwargs):
        """Create a new commit"""
        try:
            self._plan_service.add_commit(self._project)
        except PlanEmpty:
            self._ui.bold('Plan empty, abandoning.')

    def register_subparser(self, subparsers: Any):
        subparsers.add_parser(Add.subcommand, help='Add a new commit plan.')
