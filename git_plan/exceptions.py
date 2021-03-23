"""GitPlanExceptions

@author Rory Byrne <rory@rory.bio
"""


class GitPlanException(Exception):
    """Base exception for git plan"""


class CommandNotFound(GitPlanException):
    """Command doesn't exist"""


class ProjectNotInitialized(GitPlanException):
    """The project was not initialized"""


class ProjectAlreadyInitialized(GitPlanException):
    """The project is already initialized"""


class CommitAbandoned(GitPlanException):
    """The user abandoned their commit"""


class PlanEmpty(GitPlanException):
    """The commit plan was empty"""

class GitException(GitPlanException):
    """Base class for git-related exceptions"""


class NotAGitRepository(GitException):
    """The current project is not a git repository"""
