"""GitPlanExceptions

@author Rory Byrne <rory@rory.bio
"""


class GitPlanException(Exception):
    """Base exception for git plan"""


class ConfigurationError(GitPlanException):
    """Git plan is mis-configured"""


class CommandNotFound(GitPlanException):
    """Command doesn't exist"""


class NotInitialized(GitPlanException):
    """The project was not initialized"""


class AlreadyInitialized(GitPlanException):
    """The project is already initialized"""


class CommitAbandoned(GitPlanException):
    """The user abandoned their commit"""


class PlanEmpty(GitPlanException):
    """The commit plan was empty"""


class GitException(GitPlanException):
    """Base class for git-related exceptions"""


class NotAGitRepository(GitException):
    """The project is not a git repository"""
