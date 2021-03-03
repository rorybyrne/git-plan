"""CLI Entrypoint

@author Rory Byrne <rory@rory.bio>
"""
from typing import List, Dict, Optional

from git_plan.cli.commands.command import Command
from git_plan.exceptions import CommandNotFound


class CLI:
    """The command-line entrypoint"""

    def __init__(self, commands: List[Command]):
        assert not any([c.subcommand is None for c in commands]), "Command missing subcommand attribute"
        for command in commands:
            command.set_cli(self)

        self._commands: Dict[str, Command] = {c.subcommand: c for c in commands}

    def invoke(self, subcommand: str, options: Optional[Dict] = None):
        command = self.get_command(subcommand)
        command.run()

    def get_command(self, subcommand: str) -> Command:
        """Return the requested command as a singleton"""
        if not subcommand:
            subcommand = 'plan'

        command = self._commands.get(subcommand)

        if not command:
            raise CommandNotFound()

        return command
