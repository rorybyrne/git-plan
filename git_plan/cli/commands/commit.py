"""Commit command

Author: Rory Byrne <rory@rory.bio>
"""

from argparse import ArgumentParser
from typing import Any

from git_plan.cli.commands.command import Command
from git_plan.exceptions import CommitAbandoned, NoStagedFiles, PlanNotFound
from git_plan.service.git import GitService
from git_plan.service.plan import PlanService


class Commit(Command):
    """Commit a plan"""

    subcommand = "commit"

    def __init__(self, plan_service: PlanService, git_service: GitService, **kwargs):
        super().__init__(**kwargs)
        assert plan_service, "Plan service not injected"
        assert git_service, "Git service not injected"
        self._plan_service = plan_service
        self._git_service = git_service

    def command(self, plan_id: str, *args, **kwargs):
        """Create a new commit"""
        if plan_id:
            chosen_plan = self._plan_service.get_plan(plan_id)
            if not chosen_plan:
                raise PlanNotFound(plan_id)
        else:
            plans = self._plan_service.get_plans()
            if not plans:
                raise PlanNotFound("There are no plans.")
            chosen_plan = self._ui.choose_plan(plans, "Which plan do you want to commit?")

        if not self._git_service.has_staged_files():
            raise NoStagedFiles()

        try:
            self._git_service.commit(chosen_plan)
            self._plan_service.delete_plan(chosen_plan)
        except CommitAbandoned:
            print("Commit abandoned.")

    def register_subparser(self, subparsers: Any):
        parser: ArgumentParser = subparsers.add_parser(Commit.subcommand, help="Commit a plan.")
        parser.add_argument(
            "--id",
            type=str,
            dest="plan_id",
            help="The ID of the plan to be committed",
        )
