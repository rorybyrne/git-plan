"""Decorators

Author: Rory Byrne <rory@rory.bio>
"""
from functools import wraps
from typing import Callable, Type, Union

from git_plan.cli.commands.command import Command
from git_plan.exceptions import ProjectNotInitialized
from git_plan.model.commit import Commit
from git_plan.model.project import Project


def requires_initialized(ref: Union[Type[Command], Callable]):
    """Checks that the project in the arguments is initialized"""

    @wraps(ref)
    def wrapper(*args, **kwargs):
        if isinstance(ref, type):
            instance = ref(*args, **kwargs)
            instance.run = requires_initialized(instance.run)
            return instance

        # Find the project or commit argument
        if project := kwargs.get('project'):
            is_initialized = project.is_initialized()
        elif commit := kwargs.get('commit'):
            is_initialized = commit.project.is_initialized()
        elif project := next((arg for arg in args if isinstance(arg, Project)), None):
            is_initialized = project.is_initialized()
        elif commit := next((arg for arg in args if isinstance(arg, Commit)), None):
            is_initialized = commit.project.is_initialized()
        elif hasattr(ref, '__self__') and (project := getattr(ref.__self__, '_project', None)):  # command.run()
            is_initialized = project.is_initialized()
        else:
            raise RuntimeError('Cannot check for initialized project due to invalid parameters on the function')

        if is_initialized:
            return ref(*args, **kwargs)

        raise ProjectNotInitialized()

    return wrapper
