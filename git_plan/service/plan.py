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
from git_plan.model.project import Project
from git_plan.service.git import GitService
from git_plan.util.decorators import requires_initialized


class PlanService:
    """Manage the user's plans"""

    def __init__(self, commit_template_file: str, edit_template_file: str, git_service: GitService):
        assert edit_template_file, "edit_template_file missing"
        assert commit_template_file, "commit_template_file missing"
        self._commit_template_file = commit_template_file
        self._edit_template_file = edit_template_file
        self._git_service = git_service

    @requires_initialized
    def add_commit(self, project: Project):
        """Create a plan in the given directory"""
        commit_id = str(int(time.time()))
        commit = self._create_commit(project, commit_id)
        commit.save()

    @requires_initialized
    def edit_commit(self, commit: Commit):
        """Update the plan in the given directory"""
        template = self._get_template(self._edit_template_file) \
            .replace('%headline%', commit.message.headline) \
            .replace('%body%', commit.message.body)

        new_message = self._prompt_user_for_plan(initial=template)
        commit.message = new_message
        commit.save()

    @staticmethod
    @requires_initialized
    def delete_commit(commit: Commit):
        """Delete the chosen commit"""
        path = commit.path
        if not os.path.exists(path):
            raise RuntimeError(f'Commit not found: {commit}')

        os.remove(path)

    @staticmethod
    @requires_initialized
    def has_commits(project: Project) -> bool:
        """Check if a plan already exists in the given directory"""
        return project.has_commits()

    @staticmethod
    @requires_initialized
    def get_commits(project: Project) -> List[Commit]:
        """Print the status of the plan

        Raises:
            RuntimeError:   Commit file not found
        """
        return Commit.fetch_commits(project)

    # Private #############

    def _create_commit(self, project: Project, commit_id: str) -> Commit:
        message = self._prompt_user_for_plan()
        if not message or message.headline == '':
            raise RuntimeError("Invalid commit plan. Please include at least a headline.")

        branch = self._git_service.get_current_branch()
        commit = Commit(project, commit_id, branch)
        commit.message = message
        return commit

    def _prompt_user_for_plan(self, initial: str = None) -> CommitMessage:
        editor = os.environ.get('EDITOR', 'vim')
        if not initial:
            initial = self._get_template(self._commit_template_file)

        with tempfile.NamedTemporaryFile(suffix=".tmp", mode='r+') as tf:
            tf.write(initial)
            tf.flush()
            call([editor, tf.name])

            tf.seek(0)
            message_lines = tf.readlines()
            processed_input = self._post_process_commit(message_lines)

            return CommitMessage.from_string(processed_input)

    @staticmethod
    def _get_template(file: str):
        try:
            with open(file, 'r') as f:
                template = f.read()
                return template
        except FileNotFoundError as e:
            print(e)
            return ''

    @staticmethod
    def _post_process_commit(lines: List[str]):
        lines = [line.strip() for line in lines if not line.startswith('#') or line == '\n']
        if not lines or len(lines) == 0:
            raise PlanEmpty()

        headline = lines[0].strip()
        body = '\n'.join(lines[1:]).strip()

        return ''.join([headline, '\n', '\n', body])
