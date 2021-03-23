"""Git service

Author: Rory Byrne <rory@rory.bio>
"""
import subprocess

from git_plan.exceptions import CommitAbandoned, GitException
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

        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            raise CommitAbandoned() from e

    @staticmethod
    def has_staged_files() -> bool:
        """Returns True if there are staged files, and False otherwise"""
        cmd = 'git diff --staged --quiet'.split(' ')

        try:
            subprocess.run(cmd, check=True)
            return False
        except subprocess.CalledProcessError:
            return True

    @staticmethod
    def get_current_branch():
        """Gets the current branch via git"""
        cmd = 'git branch --show-current'.split(' ')

        try:
            result = subprocess.run(cmd, capture_output=True, check=True)
            branch = result.stdout.decode('utf-8')
            if not branch or branch == '':
                raise GitException(f'Invalid branch: "{branch}"')

            return branch.strip()
        except subprocess.CalledProcessError as e:
            raise GitException('Failed to get current git branch') from e
