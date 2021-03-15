"""Git utils

Author: Rory Byrne <rory@rory.bio>
"""
from git_plan.exceptions import NotAGitRepository
import os


def get_repository_root(dir: str):
    """Walks up the directory tree to find the root git dir"""
    GIT_DIR = '.git'
    prev, dir = None, os.path.abspath(dir)
    while prev != dir:
        if os.path.isdir(os.path.join(dir, GIT_DIR)):
            return dir
        prev, dir = dir, os.path.abspath(os.path.join(dir, os.pardir))

    raise NotAGitRepository()
