"""Edit command

Author: Rory Byrne <rory@rory.bio>
"""
from typing import Any

from git_plan.cli.commands.command import Command
from git_plan.service.plan import PlanService


class Edit(Command):
    """Edit an existing plan"""

    subcommand = 'edit'

    def __init__(self, plan_service: PlanService, **kwargs):
        super().__init__(**kwargs)
        self._plan_service = plan_service

    def command(self, **kwargs):
        """Edit an existing plan"""
        plans = self._plan_service.get_plans(self._project)
        if not plans:
            self._ui.bold('No plans to edit.')
            return

        chosen_plan = self._ui.choose_plan(plans, 'Which plan do you want to edit?')

        self._plan_service.edit_plan(chosen_plan)

    def register_subparser(self, subparsers: Any):
        subparsers.add_parser(Edit.subcommand, help='Edit an existing plan.')
