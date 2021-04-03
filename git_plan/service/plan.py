"""Plan service

@author Rory Byrne <rory@rory.bio>
"""
import os
import tempfile
import time
from subprocess import call
from typing import List

from git_plan.exceptions import PlanEmpty
from git_plan.model.commit import Commit, CommitMessage
from git_plan.model.repository import Repository
from git_plan.service.git import GitService
from git_plan.util.unix import is_installed


class PlanService:
    """Manage the user's plans"""

    def __init__(self, plan_template: str, edit_template: str, git_service: GitService):
        assert edit_template, "Edit template missing"
        assert plan_template, "Commit template missing"
        self._plan_template = plan_template
        self._edit_template = edit_template
        self._git_service = git_service

    def add_commit(self, repository: Repository) -> Commit:
        """Create a plan in the given directory"""
        commit_id = str(int(time.time()))
        commit = self._create_commit(repository, commit_id)
        commit.save()
        return commit

    def edit_commit(self, commit: Commit):
        """Update the plan in the given directory"""
        template = self._edit_template \
            .replace('%headline%', commit.message.headline) \
            .replace('%body%', commit.message.body)

        new_message = self._prompt_user_for_plan(initial=template)
        commit.message = new_message
        commit.updated_at = int(time.time())
        commit.save()

    @staticmethod
    def delete_commit(commit: Commit):
        """Delete the chosen commit"""
        if not commit.path.exists():
            raise RuntimeError(f'Commit not found: {commit}')

        commit.path.unlink()  # Deletes the file

    @staticmethod
    def has_commits(repository: Repository) -> bool:
        """Check if a plan already exists in the given directory"""
        return any(repository.plan_files_dir.iterdir())  # False if it cannot iterate at least once

    def get_commits(self, repository: Repository, branch: str = None) -> List[Commit]:
        """Print the status of the plan

        Raises:
            RuntimeError:   Commit file not found
        """
        return self._fetch_commits(repository, branch=branch)

    # Private #############

    def _create_commit(self, repository: Repository, commit_id: str) -> Commit:
        message = self._prompt_user_for_plan()
        if not message or message.headline == '':
            raise RuntimeError("Invalid commit plan. Please include at least a headline.")

        branch = self._git_service.get_current_branch()
        created_at: float = time.time()
        updated_at: float = created_at
        commit = Commit(repository, commit_id, branch, int(created_at), int(updated_at))
        commit.message = message
        return commit

    def _prompt_user_for_plan(self, initial: str = None) -> CommitMessage:
        if not initial:
            initial = self._plan_template

        editor = self._git_service.get_configured_editor()
        if not editor:
            editor = os.environ.get("EDITOR", "vim")
        if not is_installed(editor):
            raise RuntimeError("Couldn't find an editor installed on your system.")

        with tempfile.NamedTemporaryFile(suffix=".tmp", mode='r+') as file:
            file.write(initial)
            file.flush()
            call([editor, file.name])

            file.seek(0)
            message_lines = file.readlines()
            processed_input = self._post_process_commit(message_lines)

            return CommitMessage.from_string(processed_input)

    def _fetch_commits(self, repository: Repository, branch: str = None) -> List['Commit']:
        if not self.has_commits(repository):
            return []

        commit_files = repository.plan_files_dir.iterdir()
        commits: List[Commit] = [Commit.from_file(f, repository) for f in commit_files if f.is_file()]
        if branch:
            # .strip() for backawrds compatibility
            commits = [commit for commit in commits if commit.branch.strip() == branch]

        return commits

    @staticmethod
    def _post_process_commit(lines: List[str]):
        lines = [line.strip() for line in lines if not line.startswith('#') or line == '\n']
        if not lines or len(lines) == 0:
            raise PlanEmpty()

        headline = lines[0].strip()
        body = '\n'.join(lines[1:]).strip()

        return ''.join([headline, '\n', '\n', body])
