"""Project model

Author: Rory Byrne <rory@rory.bio>
"""
import os
from dataclasses import dataclass


@dataclass
class Project:
    root_dir: str

    def is_git_repository(self):
        return self._is_git_repository(self.root_dir)

    def has_tasks(self):
        return os.listdir(self.plan_dir)

    @property
    def plan_dir(self):
        return os.path.join(self.root_dir, '.git', 'plan')

    @classmethod
    def from_working_dir(cls, working_dir: str):
        if not cls._is_git_repository(working_dir):
            raise RuntimeError(f'{working_dir} is not a git repository.')

        return cls(working_dir)

    @staticmethod
    def _is_git_repository(directory: str) -> bool:
        return os.path.isdir(os.path.join(directory, '.git'))
