"""Decorators

Author: Rory Byrne <rory@rory.bio>
"""
from functools import wraps
from inspect import isclass

from git_plan.exceptions import NotAGitRepository, NotInitialized
from git_plan.util import unix


def requires_git_repository(ref):
    """Raises NotAGitRepository if the check for a git repository fails"""
    if isclass(ref):
        raise ValueError("@requires_git_repository can no longer be used on a class")

    @wraps(ref)
    def wrapper(self, *args, **kwargs):
        if hasattr(self, '_project'):
            if self._project is None:  # pylint: disable=protected-access
                raise RuntimeError(f"_project was None on {self.__class__.__name__}")
            if not self._project.is_a_git_repository:  # pylint: disable=protected-access
                raise NotAGitRepository()
        else:  # fallback to regular shell command
            if not unix.shell_is_in_git_repository():
                raise NotAGitRepository()

        return ref(self, *args, **kwargs)

    return wrapper


def requires_initialized(ref):
    """Checks that the repository in the arguments is initialized"""
    if isclass(ref):
        raise ValueError("@requires_initialized can no longer be used on a class")

    @wraps(ref)
    def wrapper(self, *args, **kwargs):
        if not hasattr(self, '_project'):
            raise RuntimeError(f"_project was None on {self.__class__.__name__}")

        if not self._project.is_initialized:  # pylint: disable=protected-access
            raise NotInitialized()

        return ref(self, *args, **kwargs)

    return wrapper
