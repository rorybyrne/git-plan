"""CLI Entrypoint"""
import argparse
from argparse import Namespace
from typing import Dict, List

import pkg_resources

from git_plan.cli.commands.command import Command
from git_plan.exceptions import CommandNotFound
from git_plan.model.repository import Repository
from git_plan.service.plan import PlanService


class CLI:
    """The command-line entrypoint"""

    def __init__(self, commands: List[Command], plan_service: PlanService, repository: Repository):
        assert not any(c.subcommand is None for c in commands), "Command missing subcommand attribute"
        self._plan_service = plan_service
        self._repository = repository

        self._parser = argparse.ArgumentParser(prog='git-plan', description='A better workflow for git.')
        self._parser.add_argument('subcommand', type=str, nargs='?', help='The subcommand to run')
        self._parser.add_argument('--version', dest='version', action='store_true')
        subparsers = self._parser.add_subparsers(dest='subcommand')

        for command in commands:
            command.register_subparser(subparsers)
            command.set_cli(self)

        self._commands: Dict[str, Command] = {c.subcommand: c for c in commands}

    def parse(self, args: List[str]):
        """Parse command line arguments and invoke the correct subcommand

        Args:
            args:   Command-line arguments
        """
        parsed_args = self._parse_args(args)
        if parsed_args.version:
            self.version()
            return

        if not parsed_args.subcommand:
            if self._plan_service.has_commits(self._repository):
                parsed_args.subcommand = "list"
            else:
                parsed_args.subcommand = "add"

        try:
            self.invoke(**vars(parsed_args))  # Convert to dict
        except CommandNotFound:
            self.help()

    def invoke(self, subcommand: str, **kwargs):
        """Invoke the requested subcommand and pass kwargs to it

        Args:
            subcommand:     The requested subcommand
            kwargs:         The arguments for subcommand, parsed by its subparser
        """
        command = self.get_command(subcommand)
        command.run(kwargs)

    def get_command(self, subcommand: str) -> Command:
        """Return the requested command as a singleton

        Args:
            subcommand:     The requested subcommand

        Returns:
            The corresponding instance of Command
        """
        command = self._commands.get(subcommand)

        if not command:
            raise CommandNotFound()

        return command

    @staticmethod
    def version():
        """Print the version"""
        version = pkg_resources.require('git_plan')[0]
        print(version)

    def help(self):
        """Print the help"""
        self._parser.print_help()

    def _parse_args(self, args: List[str]) -> Namespace:
        """Main entrypoint for parsing arguments.

        Args:
            args:   The commandline args to parse
        """
        parsed_args = self._parser.parse_args(args)

        return parsed_args
