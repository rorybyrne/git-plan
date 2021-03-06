"""Git service

Author: Rory Byrne <rory@rory.bio>
"""
import subprocess

from rich import print

from git_plan.model.commit import Commit


class GitService:
    """Interface to git functionality"""

    def __init__(self):
        pass

    @staticmethod
    def commit(commit: Commit):
        """Runs git commit with the given commit-plan as a template"""
        cmd = 'git commit -e -m'.split(' ')
        cmd.append(str(commit.message))

        subprocess.run(cmd)

    @staticmethod
    def has_staged_files() -> bool:
        """Returns True if there are staged files, and False otherwise"""
        cmd = 'git diff --staged --quiet'.split(' ')

        result = subprocess.run(cmd)
        return result.returncode == 1

    @staticmethod
    def get_current_branch():
        cmd = 'git branch --show-current'.split(' ')

        result = subprocess.run(cmd, capture_output=True)
        return result.stdout.decode('utf-8')
