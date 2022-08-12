"""List command

@author Rory Byrne <rory@rory.bio>
"""
from argparse import ArgumentParser
from typing import Any

from git_plan.cli.commands.command import Command
from git_plan.service.git import GitService
from git_plan.service.plan import PlanService


class List(Command):
    """List plans."""

    subcommand = 'list'

    def __init__(self, plan_service: PlanService, git_service: GitService, **kwargs):
        super().__init__(**kwargs)
        assert plan_service, "Plan service not injected"
        self._plan_service = plan_service
        self._git = git_service

    def command(self, *, long: bool = False, branch: bool = None, **kwargs):  # pylint: disable=arguments-differ
        """List the plans"""
        if branch:
            filter_branch = self._git.get_current_branch()
        else:
            filter_branch = None

        branch_display = filter_branch if filter_branch else "all branches"
        self._ui.print(f"Plans for [bold]{branch_display}[/bold]\n")
        plans = self._plan_service.get_plans(branch=filter_branch)

        if len(plans) == 0:
            if branch:
                self._ui.bold("No plans on the current branch.")
            else:
                self._ui.bold("No plans.")

            return

        plans = sorted(plans, key=lambda c: c.created_at)
        self._ui.render_plans(plans, headline_only=not long)

    def register_subparser(self, subparsers: Any):
        parser: ArgumentParser = subparsers.add_parser(List.subcommand, help='List existing plans.')
        parser.add_argument('-l', '--long', dest='long', action='store_true')
        parser.add_argument(
            '-b',
            '--branch',
            dest='branch',
            action='store_true',
            help='Show plans for the current branch'
        )
