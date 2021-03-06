"""Help command

@author Rory Byrne <rory@rory.bio>
"""
from typing import Any

from git_plan.cli.commands.command import Command


class Help(Command):
    """Print the help"""

    subcommand = 'help'

    def __init__(self):
        super().__init__()

    def pre_command(self):
        """Perhaps some validation?"""
        pass

    def command(self):
        """Create a new commit"""
        self._cli.help()

    def register_subparser(self, subparsers: Any):
        subparsers.add_parser(Help.subcommand, help='Print the help.')
