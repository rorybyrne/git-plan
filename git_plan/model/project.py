"""Project model

Author: Rory Byrne <rory@rory.bio>
"""
from dataclasses import dataclass
from pathlib import Path

from git_plan.exceptions import NotAGitRepository
from git_plan.util.git import get_repository_root


@dataclass
class Project:
    """A project that the user is working on"""
    root_dir: Path

    @property
    def plan_dir(self) -> Path:
        """The directory where this project's plans are stored"""
        return Path(self.root_dir) / '.git' / 'plan'

    def is_initialized(self) -> bool:
        """Returns true if the project has a plan directory and git initialized"""
        return Path(self.plan_dir).exists() and self.is_git_repository()

    def is_git_repository(self) -> bool:
        """Checks whether the project is a git repository"""
        try:
            get_repository_root(self.root_dir)
            return True
        except NotAGitRepository:
            return False
