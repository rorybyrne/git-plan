"""
Kill command

@author Rory Byrne <rory@rory.bio>
"""
from git_plan.commands.command import Command


class Kill(Command):
    """Kill existing observer"""

    def pre_command(self):
        """Check that an observer is active for this repository"""
        pass

    def command(self):
        """Use the ObserverService to kill the observer"""
        pass
