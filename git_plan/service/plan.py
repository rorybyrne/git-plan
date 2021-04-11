"""Plan service

@author Rory Byrne <rory@rory.bio>
"""
import os
import tempfile
import time
from subprocess import call
from typing import List

from git_plan.exceptions import PlanEmpty
from git_plan.model.plan import Plan, PlanMessage
from git_plan.model.repository import Repository
from git_plan.service.git import GitService
from git_plan.util.unix import is_installed


class PlanService:
    """Manage the user's plans"""

    def __init__(self, plan_template: str, edit_template: str, git_service: GitService):
        assert edit_template, "Edit template missing"
        assert plan_template, "Plan template missing"
        self._plan_template = plan_template
        self._edit_template = edit_template
        self._git_service = git_service

    def add_plan(self, repository: Repository) -> Plan:
        """Create a plan in the given directory"""
        plan_id = str(int(time.time()))
        plan = self._create_plan(repository, plan_id)
        plan.save()
        return plan

    def edit_plan(self, plan: Plan):
        """Update the plan in the given directory"""
        template = self._edit_template \
            .replace('%headline%', plan.message.headline) \
            .replace('%body%', plan.message.body)

        new_message = self._prompt_user_for_plan(initial=template)
        plan.message = new_message
        plan.updated_at = int(time.time())
        plan.save()

    @staticmethod
    def delete_plan(plan: Plan):
        """Delete the chosen plan"""
        if not plan.path.exists():
            raise RuntimeError(f'Plan not found: {plan}')

        plan.path.unlink()  # Deletes the file

    @staticmethod
    def has_plans(repository: Repository) -> bool:
        """Check if a plan already exists in the given directory"""
        return any(repository.plan_files_dir.iterdir())  # False if it cannot iterate at least once

    def get_plans(self, repository: Repository, branch: str = None) -> List[Plan]:
        """Print the status of the plan

        Raises:
            RuntimeError:   Plan file not found
        """
        return self._fetch_plans(repository, branch=branch)

    # Private #############

    def _create_plan(self, repository: Repository, plan_id: str) -> Plan:
        message = self._prompt_user_for_plan()
        if not message or message.headline == '':
            raise RuntimeError("Invalid plan. Please include at least a headline.")

        branch = self._git_service.get_current_branch()
        created_at: float = time.time()
        updated_at: float = created_at
        plan = Plan(repository, plan_id, branch, int(created_at), int(updated_at))
        plan.message = message
        return plan

    def _prompt_user_for_plan(self, initial: str = None) -> PlanMessage:
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
            processed_input = self._post_process_plan(message_lines)

            return PlanMessage.from_string(processed_input)

    def _fetch_plans(self, repository: Repository, branch: str = None) -> List['Plan']:
        if not self.has_plans(repository):
            return []

        plan_files = repository.plan_files_dir.iterdir()
        plans: List[Plan] = [Plan.from_file(f, repository) for f in plan_files if f.is_file()]
        if branch:
            # .strip() for backawrds compatibility
            plans = [plan for plan in plans if plan.branch.strip() == branch.strip()]

        return plans

    @staticmethod
    def _post_process_plan(lines: List[str]):
        lines = [line.strip() for line in lines if not line.startswith('#') or line == '\n']
        if not lines or len(lines) == 0:
            raise PlanEmpty()

        headline = lines[0].strip()
        body = '\n'.join(lines[1:]).strip()

        return ''.join([headline, '\n', '\n', body])
