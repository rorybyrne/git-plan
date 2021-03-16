"""Git utils

Author: Rory Byrne <rory@rory.bio>
"""
from pathlib import Path

from git_plan.exceptions import NotAGitRepository

GIT_DIR = '.git'


def get_repository_root(directory: Path):
    """Walks up the directory tree to find the root git dir

    Note:
        Technically, this will return true on a non-git repository if it has a .git/ directory
        ...But who would ever do that?
    """
    prev, directory = None, Path(directory).resolve()
    while prev != directory:
        if (directory / GIT_DIR).exists():
            return directory.resolve()
        prev, directory = directory, directory.parent

    raise NotAGitRepository()
