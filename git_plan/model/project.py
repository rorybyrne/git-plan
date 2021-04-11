"""Project model

Author: Rory Byrne <rory@rory.bio>
"""
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from git_plan.exceptions import NotAGitRepository
from git_plan.util.git import get_repository_root


@dataclass
class Project:
    """A project"""
    root_dir: Path

    @property
    def plan_dir(self) -> Path:
        """This project's .plan/ directory"""
        return Path(self.root_dir) / '.plan'

    @property
    def plan_files_dir(self) -> Path:
        """The directory where this project's plans are stored"""
        return self.plan_dir / "plans"

    @property
    def is_initialized(self) -> bool:
        """Returns true if the project has a plan directory"""
        return self.plan_dir.exists() and self.plan_files_dir.exists()

    @property
    def is_a_git_repository(self) -> bool:
        try:
            get_repository_root(self.root_dir)
            return True
        except NotAGitRepository:
            return False

    @classmethod
    def from_dir(cls, directory: Path) -> Optional["Project"]:
        """Returns a Project with the directory as its root"""
        return cls(directory)
