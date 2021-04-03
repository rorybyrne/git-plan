"""GitPlanExceptions

@author Rory Byrne <rory@rory.bio
"""


class GitPlanException(Exception):
    """Base exception for git plan"""


class CommandNotFound(GitPlanException):
    """Command doesn't exist"""


class NotInitialized(GitPlanException):
    """The repo was not initialized"""


class AlreadyInitialized(GitPlanException):
    """The repo is already initialized"""


class CommitAbandoned(GitPlanException):
    """The user abandoned their commit"""


class PlanEmpty(GitPlanException):
    """The commit plan was empty"""


class GitException(GitPlanException):
    """Base class for git-related exceptions"""


class NotAGitRepository(GitException):
    """The current repo is not a git repository"""
