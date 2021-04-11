"""Init command

@author Rory Byrne <rory@rory.bio>
"""
from typing import Any

from git_plan.cli.commands.command import Command
from git_plan.exceptions import AlreadyInitialized
from git_plan.service.repository import RepositoryService
from git_plan.util.decorators import requires_git_repository


@requires_git_repository
class Init(Command):
    """Initialize git plan in the directory."""

    subcommand = 'init'

    def __init__(self, repository_service: RepositoryService, **kwargs):
        super().__init__(**kwargs)
        assert repository_service, "Repository service not injected"
        self._repo_service = repository_service

    def command(self, **kwargs):
        """Initialize the repository if it is not already initialized"""
        if not self._repository:
            self._ui.bold("Not in a git repository.")
            return

        try:
            self._repo_service.initialize(self._repository)
            self._ui.print(f"Initialized git plan in [bold]{self._repository.plan_dir}[/bold]")
        except AlreadyInitialized:
            self._ui.bold("Git plan is already initialized.")

    def register_subparser(self, subparsers: Any):
        subparsers.add_parser(Init.subcommand, help='Initialize git plan.')
