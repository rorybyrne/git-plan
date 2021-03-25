"""Init command

@author Rory Byrne <rory@rory.bio>
"""
from typing import Any

from git_plan.cli.commands.command import Command
from git_plan.exceptions import ProjectAlreadyInitialized
from git_plan.service.project import ProjectService


class Init(Command):
    """Initialize git plan in the directory."""

    subcommand = 'init'

    def __init__(self, project_service: ProjectService, **kwargs):
        super().__init__(**kwargs)
        assert project_service, "Project service not injected"
        self._project_service = project_service

    def command(self, **kwargs):
        """Initialize the project if it is not already initialized"""
        if not self._project.is_git_repository():
            self._ui.bold("Not in a git repository.")
            return

        try:
            self._project_service.initialize(self._project)
            self._ui.print(f"Initialized git plan in [bold]{self._project.plan_dir}[/bold]")
        except ProjectAlreadyInitialized:
            self._ui.bold("Git plan is already initialized.")

    def register_subparser(self, subparsers: Any):
        subparsers.add_parser(Init.subcommand, help='Initialize git plan.')
