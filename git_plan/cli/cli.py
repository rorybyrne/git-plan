"""CLI Entrypoint

@author Rory Byrne <rory@rory.bio>
"""
import argparse
from argparse import Namespace
from typing import List, Dict

from git_plan.cli.commands.command import Command
from git_plan.exceptions import CommandNotFound


class CLI:
    """The command-line entrypoint"""

    def __init__(self, commands: List[Command]):
        assert not any([c.subcommand is None for c in commands]), "Command missing subcommand attribute"

        self._parser = argparse.ArgumentParser(prog='git-plan', description='A better workflow for git.')
        self._parser.add_argument('subcommand', type=str, nargs='?', help='The subcommand to run')
        subparsers = self._parser.add_subparsers(dest='subcommand')

        for command in commands:
            command.register_subparser(subparsers)
            command.set_cli(self)

        self._commands: Dict[str, Command] = {c.subcommand: c for c in commands}

    def parse(self, args: List[str]):
        parsed_args = self._parse_args(args)

        try:
            self.invoke(**vars(parsed_args))  # Convert to dict
        except CommandNotFound as e:
            print(e)
            self._parser.print_help()
        except RuntimeError:
            raise

    def invoke(self, subcommand: str, **kwargs: dict):
        command = self.get_command(subcommand)
        command.run(kwargs)

    def get_command(self, subcommand: str) -> Command:
        """Return the requested command as a singleton"""
        command = self._commands.get(subcommand)

        if not command:
            raise CommandNotFound()

        return command

    def _parse_args(self, args: List[str]):
        parsed_args = self._parser.parse_args(args)
        parsed_args.subcommand = parsed_args.subcommand or 'plan'

        return parsed_args
