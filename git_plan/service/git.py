"""Git service

Author: Rory Byrne <rory@rory.bio>
"""
import subprocess
from typing import Optional

from git_plan.exceptions import CommitAbandoned, GitException
from git_plan.model.commit import Commit
from git_plan.util import unix
from git_plan.util.decorators import requires_git_repository


class GitService:
    """Interface to git functionality"""

    COMMIT = 'git commit -e -m'
    HAS_STAGED = 'git diff --staged --quiet'
    GET_BRANCH = 'git branch --show-current'
    CONFIGURED_GIT_EDITOR = 'git config --global core.editor'

    def __init__(self):
        pass

    @requires_git_repository
    def commit(self, commit: Commit):
        """Runs git commit with the given commit-plan as a template"""
        cmd = self.COMMIT.split(' ')
        cmd.append(str(commit.message))

        try:
            unix.run_command(cmd, capture_output=False)
        except subprocess.CalledProcessError as e:
            raise CommitAbandoned() from e

    @requires_git_repository
    def has_staged_files(self) -> bool:
        """Returns True if there are staged files, and False otherwise"""
        cmd = self.HAS_STAGED.split(' ')

        try:
            unix.run_command(cmd)
            return False
        except subprocess.CalledProcessError:
            return True

    @requires_git_repository
    def get_current_branch(self):
        """Gets the current branch via git"""
        cmd = self.GET_BRANCH.split(' ')

        try:
            branch = unix.run_command(cmd)
            if not branch or branch == '':
                raise GitException(f'Invalid branch: "{branch}"')

            return branch.strip()
        except subprocess.CalledProcessError as e:
            raise GitException('Failed to get current git branch') from e

    @requires_git_repository
    def get_configured_editor(self) -> Optional[str]:
        """Gets the editor configured for git"""
        cmd = self.CONFIGURED_GIT_EDITOR.split(' ')

        try:
            editor = unix.run_command(cmd)
            return editor.strip() if editor else None
        except subprocess.CalledProcessError:
            return None
