"""Base class for Commands

@author Rory Byrne <rory@rory.bio>
"""
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional, Any

from git_plan.model.repository import Repository
from git_plan.service.ui import UIService

if TYPE_CHECKING:
    from git_plan.cli.cli import CLI
else:
    CLI = Any


class Command(ABC):
    """Base for all Commands"""

    subcommand: str

    def __init__(self, repository: Optional[Repository], ui_service: UIService):
        self._cli: Optional[CLI] = None
        self._repository: Optional[Repository] = repository
        self._ui = ui_service

    def run(self, context: dict):
        """Run the command"""
        self.command(**context)

    def set_cli(self, cli: 'CLI'):
        """Set the CLI reference, so that a command can trigger other commands"""
        assert cli, "Cannot set CLI: None"
        self._cli = cli

    @abstractmethod
    def register_subparser(self, subparsers: Any):
        """Allows a command to define its own args"""
        raise NotImplementedError()

    @abstractmethod
    def command(self, **kwargs):
        """The implementation of the command's functionality"""
        raise NotImplementedError()
