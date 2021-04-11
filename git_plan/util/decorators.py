"""Decorators

Author: Rory Byrne <rory@rory.bio>
"""
import subprocess
from functools import wraps
from inspect import isclass

from git_plan.exceptions import NotAGitRepository, NotInitialized
from git_plan.util import unix


def _shell_is_in_git_repository():
    command = 'git rev-parse --is-inside-work-tree'
    cmd = command.split(' ')
    try:
        unix.run_command(cmd)
        return True
    except subprocess.CalledProcessError:
        return False


def requires_git_repository(ref):
    """Raises NotAGitRepository if the check for a git repository fails"""
    if isclass(ref):
        if not hasattr(ref, 'run'):
            raise ValueError("Cannot use @requires_git_repository on this class")
        ref.run = requires_git_repository(ref.run)
        return ref

    @wraps(ref)
    def wrapper(self, *args, **kwargs):
        if hasattr(self, '_repository'):
            if self._repository is None:  # pylint: disable=protected-access
                raise NotAGitRepository()
        else:  # fallback to regular shell command
            if not _shell_is_in_git_repository():
                raise NotAGitRepository()

        return ref(self, *args, **kwargs)

    return wrapper


def requires_initialized(ref):
    """Checks that the repository in the arguments is initialized"""
    if isclass(ref):
        if not hasattr(ref, 'run'):
            raise ValueError("Cannot use @requires_initialized on this class")
        ref.run = requires_initialized(ref.run)
        return ref

    @wraps(ref)
    def wrapper(self, *args, **kwargs):
        if not hasattr(self, '_repository'):
            raise ValueError("Cannot use the @requires_initialized decorator here.")

        if self._repository is None:  # pylint: disable=protected-access
            raise NotAGitRepository()

        is_initialized = self._repository.is_initialized()  # pylint: disable=protected-access

        if is_initialized:
            return ref(self, *args, **kwargs)

        raise NotInitialized()

    return wrapper
