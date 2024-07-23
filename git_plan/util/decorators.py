"""Decorators

Author: Rory Byrne <rory@rory.bio>
"""

from functools import wraps
from inspect import isclass

from git_plan.exceptions import NotAGitRepository, NotInitialized
from git_plan.model.project import Project
from git_plan.util import unix


def requires_git_repository(ref):
    """Raises NotAGitRepository if the check for a git repository fails"""
    if isclass(ref):
        raise ValueError("@requires_git_repository can no longer be used on a class")

    @wraps(ref)
    def wrapper(self, *args, **kwargs):
        if not unix.shell_is_in_git_repository():
            raise NotAGitRepository()

        return ref(self, *args, **kwargs)

    return wrapper


def requires_initialized(ref):
    """Checks that the repository in the arguments is initialized"""
    if isclass(ref):
        raise ValueError("deprecated: @requires_initialized can no longer be used on a class")

    @wraps(ref)
    def wrapper(self, *args, **kwargs):
        project: Project = getattr(self, "_project", None)
        if not project.is_initialized:
            raise NotInitialized()

        return ref(self, *args, **kwargs)

    return wrapper
