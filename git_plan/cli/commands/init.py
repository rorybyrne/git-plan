"""Init command

@author Rory Byrne <rory@rory.bio>
"""
from typing import Any

from git_plan.cli.commands.command import Command
from git_plan.service.project import ProjectService
from git_plan.service.ui import UIService


class Init(Command):
    """Initialize git plan in the directory."""

    subcommand = 'init'

    def __init__(self, ui_service: UIService, project_service: ProjectService, **kwargs):
        super().__init__(**kwargs)
        assert project_service, "Project service not injected"
        self._project_service = project_service
        self._ui_service = ui_service

    def pre_command(self):
        """Check whether a plan already exists?"""
        pass

    def command(self, **kwargs):
        """Initialize the project if it is not already initialized"""
        if self._project.is_initialized():
            self._ui_service.bold("Git plan is already initialized.")
            return
        else:
            self._project_service.initialize(self._project)
            self._ui_service.bold("Initialized git plan.")

    def register_subparser(self, subparsers: Any):
        subparsers.add_parser(Init.subcommand, help='Initialize git plan.')
