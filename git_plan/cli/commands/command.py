"""Base class for Commands

@author Rory Byrne <rory@rory.bio>
"""
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional, List, Any

from git_plan.model.project import Project
from git_plan.service.ui import UIService

if TYPE_CHECKING:
    from git_plan.cli.cli import CLI


class Command(ABC):

    subcommand: str = None

    def __init__(self, project: Project = None, ui_service: UIService = None, *args, **kwargs):
        assert project, "Project missing."
        assert ui_service, "UI service missing"
        self._cli: Optional[CLI] = None
        self._project = project
        self._ui = ui_service

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
