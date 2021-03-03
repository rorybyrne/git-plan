"""Add command

@author Rory Byrne <rory@rory.bio>
"""
from git_plan.cli.commands.command import Command
from git_plan.model.project import Project
from git_plan.service.plan import PlanService


class Add(Command):
    """Add a new commit"""

    subcommand = 'add'

    def __init__(self, plan_service: PlanService, working_dir: str):
        assert plan_service, "Plan service not injected"
        assert working_dir, "Working dir not injected"
        self._plan_service = plan_service
        self._project = Project.from_working_dir(working_dir)

    def pre_command(self):
        """Perhaps some validation?"""
        pass

    def command(self):
        """Create a new commit"""
        self._plan_service.create_commit(self._project)
