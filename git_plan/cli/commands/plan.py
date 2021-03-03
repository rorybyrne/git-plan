"""Plan command

@author Rory Byrne <rory@rory.bio>
"""
from argparse import ArgumentParser
from typing import Any

from git_plan.exceptions import CommandNotFound
from git_plan.cli.commands.command import Command
from git_plan.model.project import Project
from git_plan.service.plan import PlanService
from git_plan.service.ui import UIService


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

    def command(self):
        """Use the PlanService to create the plan in the local .git/ directory

        1. Present a VIM editor with the PLAN_MSG template
        2. Save the result to a stable location
        3. Launch an observer to watch the development environment
            3a. When does the observer terminate?
        """
        if self._plan_service.has_commits(self._project):
            try:
                return self._cli.invoke('list')
            except CommandNotFound as e:
                print("OOPS GIT PLAN IS BROKEN.")
                print(e)

        self._plan_service.create_commit(self._project)

    def register_subparser(self, subparsers: Any):
        subparsers.add_parser(Plan.subcommand, help='Add a new commit, or view existing ones.')
