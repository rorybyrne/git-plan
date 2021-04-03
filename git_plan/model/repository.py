"""Repository model

Author: Rory Byrne <rory@rory.bio>
"""
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from git_plan.exceptions import NotAGitRepository
from git_plan.util.git import get_repository_root


@dataclass
class Repository:
    """A git repository"""
    root_dir: Path

    @property
    def plan_dir(self) -> Path:
        """This repo's .plan/ directory"""
        return Path(self.root_dir) / '.plan'

    @property
    def plan_files_dir(self) -> Path:
        """The directory where this repo's plans are stored"""
        return self.plan_dir / "plans"

    def is_initialized(self) -> bool:
        """Returns true if the repo has a plan directory"""
        return self.plan_dir.exists() and self.plan_files_dir.exists()

    @classmethod
    def from_working_dir(cls, working_dir: Path) -> Optional["Repository"]:
        """Constructs a Repository if in a git repository, otherwise returns None"""
        try:
            repo_root = get_repository_root(working_dir)
            return cls(repo_root)
        except NotAGitRepository:
            return None
