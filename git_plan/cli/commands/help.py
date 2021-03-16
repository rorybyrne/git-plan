"""Help command

@author Rory Byrne <rory@rory.bio>
"""
from typing import Any

from git_plan.cli.commands.command import Command


class Help(Command):  # pylint: disable=too-few-public-methods
    """Print the help"""

    subcommand = 'help'

    def command(self, **kwargs):
        """Create a new commit"""
        self._cli.help()

    def register_subparser(self, subparsers: Any):
        subparsers.add_parser(Help.subcommand, help='Print the help.')
