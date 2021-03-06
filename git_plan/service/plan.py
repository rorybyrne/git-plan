"""Plan service

@author Rory Byrne <rory@rory.bio>
"""
import os
import tempfile
import time
from subprocess import call
from typing import List

from git_plan.model.commit import Commit, CommitMessage
from git_plan.model.project import Project
from git_plan.service.git import GitService


class PlanService:
    """Manage the user's plans"""

    def __init__(self, plan_home: str, commit_template_file: str, git_service: GitService, edit_template_file: str):
        assert commit_template_file, "Commit template filename missing"
        self._commit_template_file = os.path.join(plan_home, commit_template_file)
        self._edit_template_file = os.path.join(plan_home, edit_template_file)
        self._git_service = git_service
        self._plan_home = plan_home

    def create_commit(self, project: Project):
        """Create a plan in the given directory

        1. Create a new file in .git/ containing the plan
        """
        if not project.is_initialized():
            self._initialize_project(project)
        message = self._plan_commit()
        commit_id = str(int(time.time()))
        branch = self._git_service.get_current_branch()
        commit = Commit(project, commit_id, branch)
        commit.message = message
        commit.save()

    def edit_commit(self, commit: Commit):
        """Update the plan in the given directory"""
        template = self._get_template(self._edit_template_file) \
            .replace('%headline%', commit.message.headline) \
            .replace('%body%', commit.message.body)

        new_message = self._plan_commit(initial=template)
        commit.message = new_message
        commit.save()

    def delete_commit(self, commit: Commit):
        """Delete the chosen commit"""
        path = commit.path
        if not os.path.exists(path):
            raise RuntimeError(f'Commit not found: {commit}')

        os.remove(path)

    def has_commits(self, project: Project) -> bool:
        """Check if a plan already exists in the given directory"""
        if not project.is_initialized():
            self._initialize_project(project)
        return project.has_commits()

    def get_commits(self, project: Project) -> List[Commit]:
        """Print the status of the plan

        Raises:
            RuntimeError:   Commit file not found
        """
        if not project.is_initialized():
            self._initialize_project(project)
        return Commit.fetch_commits(project)

    # Private #############

    def _plan_commit(self, initial: str = None) -> CommitMessage:
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
        headline = lines[0].strip()
        body = '\n'.join(lines[1:]).strip()

        return ''.join([headline, '\n', '\n', body])

    @staticmethod
    def _initialize_project(project: Project):
        plan_dir = project.plan_dir
        if os.path.exists(plan_dir):
            print("Project already initialized.")
            return

        os.mkdir(plan_dir)

