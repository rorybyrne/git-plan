"""Exceptions

@author Rory Byrne <rory@rory.bio
"""


class CommandNotFound(Exception):
    """Command doesn't exist"""


class ProjectNotInitialized(Exception):
    """The project was not initialized"""


class CommitAbandoned(Exception):
    """The user abandoned their commit"""


class PlanEmpty(Exception):
    """The commit plan was empty"""

class NotAGitRepository(Exception):
    """The current project is not a git repository"""
