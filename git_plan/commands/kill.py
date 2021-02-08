"""Kill command

@author Rory Byrne <rory@rory.bio>
"""
from git_plan.commands.command import Command
from git_plan.service.observer import ObserverService


class Kill(Command):
    """Kill existing observer"""

    subcommand = 'kill'

    def __init__(self, observer_service: ObserverService):
        self._observer_service = observer_service

    def pre_command(self):
        """Check that an observer is active for this repository"""
        pass

    def command(self):
        """Use the ObserverService to kill the observer"""
        pass
