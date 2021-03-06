"""Plan command

@author Rory Byrne <rory@rory.bio>
"""
from typing import Any

from git_plan.cli.commands.command import Command
from git_plan.exceptions import CommandNotFound
from git_plan.model.project import Project
from git_plan.service.plan import PlanService


class Plan(Command):
    """Create or update a plan."""

    subcommand = 'plan'

    def __init__(self, plan_service: PlanService, working_dir: str):
        super().__init__()
        assert plan_service, "Plan service not injected"
        assert working_dir, "Working dir not injected"
        self._plan_service = plan_service
        self._project = Project.from_working_dir(working_dir)

    def pre_command(self):
        """Check whether a plan already exists?"""
        pass

    def command(self, **kwargs):
        """Plan a commit"""
        if self._plan_service.has_commits(self._project):
            try:
                return self._cli.invoke('list', **kwargs)
            except CommandNotFound as e:
                print("OOPS GIT PLAN IS BROKEN.")
                print(e)
        else:
            self._cli.invoke('add', **kwargs)

    def register_subparser(self, subparsers: Any):
        subparsers.add_parser(Plan.subcommand, help='Add a new commit, or view existing ones.')
