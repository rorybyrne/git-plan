"""
Base class for Commands

@author Rory Byrne <rory@rory.bio>
"""
from abc import ABC, abstractmethod


class Command(ABC):

    @classmethod
    def run(cls):
        command = cls()
        command.pre_command()
        command.command()

    @abstractmethod
    def pre_command(self):
        raise NotImplementedError()

    @abstractmethod
    def command(self):
        raise NotImplementedError()
