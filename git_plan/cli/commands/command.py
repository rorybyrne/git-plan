"""Base class for Commands

@author Rory Byrne <rory@rory.bio>
"""
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional, List, Any

if TYPE_CHECKING:
    from git_plan.cli.cli import CLI


class Command(ABC):

    subcommand: str = None

    def __init__(self):
        self._cli: Optional[CLI] = None

    def run(self, context: dict):
        self.pre_command()
        self.command(**context)

    def set_cli(self, cli: 'CLI'):
        assert cli, "Cannot set CLI: None"
        self._cli = cli

    @abstractmethod
    def register_subparser(self, subparsers: Any):
        raise NotImplementedError()

    @abstractmethod
    def pre_command(self):
        raise NotImplementedError()

    @abstractmethod
    def command(self, **kwargs):
        raise NotImplementedError()
