"""Git service

Author: Rory Byrne <rory@rory.bio>
"""
import subprocess
from typing import List, Optional

from git_plan.exceptions import CommitAbandoned, GitException
from git_plan.model.commit import Commit


class GitService:
    """Interface to git functionality"""

    COMMIT = 'git commit -e -m'
    HAS_STAGED = 'git diff --staged --quiet'
    GET_BRANCH = 'git branch --show-current'

    def __init__(self):
        pass

    def commit(self, commit: Commit):
        """Runs git commit with the given commit-plan as a template"""
        cmd = self.COMMIT.split(' ')
        cmd.append(str(commit.message))

        try:
            self._run_command(cmd, capture_output=False)
        except subprocess.CalledProcessError as e:
            raise CommitAbandoned() from e

    def has_staged_files(self) -> bool:
        """Returns True if there are staged files, and False otherwise"""
        cmd = self.HAS_STAGED.split(' ')

        try:
            self._run_command(cmd)
            return False
        except subprocess.CalledProcessError:
            return True

    def get_current_branch(self):
        """Gets the current branch via git"""
        cmd = self.GET_BRANCH.split(' ')

        try:
            branch = self._run_command(cmd)
            if not branch or branch == '':
                raise GitException(f'Invalid branch: "{branch}"')

            return branch.strip()
        except subprocess.CalledProcessError as e:
            raise GitException('Failed to get current git branch') from e

    @staticmethod
    def _run_command(cmd: List[str], capture_output: bool = True) -> Optional[str]:
        result = subprocess.run(cmd, capture_output=capture_output, check=True)
        if result.stdout:
            return result.stdout.decode()

        return None
