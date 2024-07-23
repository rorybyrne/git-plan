"""GitPlanExceptions

@author Rory Byrne <rory@rory.bio
"""


class GitPlanException(Exception):
    """An error occurred:"""

    def __str__(self) -> str:
        docstring = self.__doc__ or "An error occurred."
        message = f"\t{self.args[0]}" if self.args else ""
        return docstring + message


class ConfigurationError(GitPlanException):
    """Git plan is mis-configured:"""


### Commands


class CommandNotFound(GitPlanException):
    """Command doesn't exist:"""


### Project


class NotInitialized(GitPlanException):
    """The project was not initialized."""


class AlreadyInitialized(GitPlanException):
    """The project is already initialized."""


### Plans


class CommitAbandoned(GitPlanException):
    """You abandoned the commit."""


class PlanEmpty(GitPlanException):
    """The commit plan was empty."""


class NotFound(GitPlanException):
    """Not found:"""


class PlanNotFound(NotFound):
    """Plan not found:"""


### Git


class GitException(GitPlanException):
    """An error occurred in git."""


class NotAGitRepository(GitException):
    """The project is not a git repository"""


class NoStagedFiles(GitException):
    """No staged files."""
