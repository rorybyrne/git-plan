"""Delete command

Author: Rory Byrne <rory@rory.bio>
"""
from typing import Any

from git_plan.cli.commands.command import Command
from git_plan.service.plan import PlanService


class Delete(Command):
    """Delete an existing plan"""

    subcommand = 'delete'

    def __init__(self, plan_service: PlanService, **kwargs):
        super().__init__(**kwargs)
        assert plan_service, "Plan service not injected"
        self._plan_service = plan_service

    def command(self, **kwargs):
        """Create a new plan"""
        plans = self._plan_service.get_plans(self._project)
        if not plans:
            self._ui.bold('No plans found.')
            return

        chosen_plan = self._ui.choose_plan(plans, 'Which plan do you want to delete?')

        self._ui.bold(f'{chosen_plan.message.headline}\n')
        confirm_msg = 'Are you sure you want to delete this plan?'
        if not self._ui.confirm(confirm_msg):
            self._ui.bold("Stopped.")
            return

        self._plan_service.delete_plan(chosen_plan)
        self._ui.bold('Deleted.')

    def register_subparser(self, subparsers: Any):
        subparsers.add_parser(Delete.subcommand, help='Delete a plan.')
