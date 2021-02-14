"""Base class for Commands

@author Rory Byrne <rory@rory.bio>
"""
from abc import ABC, abstractmethod


class Command(ABC):

    subcommand: str = None

    def run(self):
        self.pre_command()
        self.command()

    @abstractmethod
    def pre_command(self):
        raise NotImplementedError()

    @abstractmethod
    def command(self):
        raise NotImplementedError()
