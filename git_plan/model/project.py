"""Project model

Author: Rory Byrne <rory@rory.bio>
"""
from git_plan.exceptions import NotAGitRepository
from git_plan.util.git import get_repository_root
import os
from dataclasses import dataclass


@dataclass
class Project:
    root_dir: str

    @property
    def plan_dir(self):
        return os.path.join(self.root_dir, '.git', 'plan')

    def is_initialized(self) -> bool:
        return os.path.exists(self.plan_dir) and self.is_git_repository()

    def is_git_repository(self) -> bool:
        try:
            get_repository_root(self.root_dir)
            return True
        except NotAGitRepository:
            return False
