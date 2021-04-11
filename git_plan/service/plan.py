"""Plan service

@author Rory Byrne <rory@rory.bio>
"""
import os
import tempfile
import time
from subprocess import call
from typing import List, Optional

from git_plan.exceptions import NotInitialized, PlanEmpty
from git_plan.model.plan import Plan, PlanId, PlanMessage
from git_plan.model.project import Project
from git_plan.service.git import GitService
from git_plan.service.provider import ProviderService
from git_plan.service.providers import Provider
from git_plan.util.decorators import requires_initialized
from git_plan.util.unix import is_installed


class PlanService:
    """Manage the user's plans"""

    def __init__(
            self,
            plan_template: str,
            edit_template: str,
            git_service: GitService,
            provider_service: ProviderService,
            project: Project
    ):
        assert edit_template, "Edit template missing"
        assert plan_template, "Plan template missing"
        self._plan_template = plan_template
        self._edit_template = edit_template
        self._git_service = git_service
        self._provider_service = provider_service
        self._project = project

    @requires_initialized
    def add_plan(self) -> Plan:
        """Create a plan in the given directory

        Prompts the user to create a new plan, and then generates an ID for the plan. The ID
        is generated using the ID strategy for the current project.
        """
        provider = self._provider_service.get_local_provider()
        plan_id = self._generate_next_id(provider)
        plan = self._create_plan(self._project, plan_id)
        plan.save()
        return plan

    #  def import_plan(self, project: Project, provider: PlanProvider, issue_id: str) -> Plan:
        """Import a plan from a plan provider

        First, we get the specific plan provider, then we try to import the issue by ID and create
        a plan instance from it.
        """
        #  provider = self._provider_service.get_by_name(provider_name)
        #  plan = provider.from_id(issue_id)

    @requires_initialized
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
    @requires_initialized
    def delete_plan(plan: Plan):
        """Delete the chosen plan"""
        if not plan.path.exists():
            raise RuntimeError(f'Plan not found: {plan}')

        plan.path.unlink()  # Deletes the file

    @requires_initialized
    def has_plans(self) -> bool:
        """Check if a plan already exists in the given directory"""
        return any(self._project.plan_files_dir.iterdir())  # False if it cannot iterate at least once

    @requires_initialized
    def get_plans(self, branch: str = None) -> List[Plan]:
        """Print the status of the plan

        Raises:
            RuntimeError:   Plan file not found
        """
        return self._fetch_plans(self._project, branch=branch)

    # Private #############

    def _generate_next_id(self, provider: Provider) -> PlanId:
        """Generate the next ID for the project"""
        latest_plan = self._get_latest_plan()
        return provider.generate_id(latest_plan)

    def _get_latest_plan(self) -> Optional[Plan]:
        """Get the plan with the highest ID number"""
        plans = self._fetch_plans(self._project, branch=None)
        if len(plans) == 0:
            return None
        elif len(plans) == 1:
            return plans[0]
        else:
            return sorted(plans, key=lambda plan: plan.id.number)[0]

    def _create_plan(self, project: Project, plan_id: PlanId) -> Plan:
        message = self._prompt_user_for_plan()
        if not message or message.headline == '':
            raise RuntimeError("Invalid plan. Please include at least a headline.")

        branch = self._git_service.get_current_branch()
        created_at: float = time.time()
        updated_at: float = created_at
        plan = Plan(project, plan_id, branch, int(created_at), int(updated_at))
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

    def _fetch_plans(self, project: Project, branch: str = None) -> List['Plan']:
        if not self.has_plans():
            return []

        plan_files = project.plan_files_dir.iterdir()
        plans: List[Plan] = [Plan.from_file(f, project) for f in plan_files if f.is_file()]
        if branch:
            # .strip() for backwards compatibility
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
