"""Plan service

@author Rory Byrne <rory@rory.bio>
"""

import os
import subprocess
import tempfile
import time
from pathlib import Path
from subprocess import CalledProcessError
from typing import Dict, Iterable, List, Optional

from git_plan.exceptions import GitPlanException, NotInitialized, PlanEmpty
from git_plan.model.plan import Plan, PlanId, PlanMessage
from git_plan.model.project import Project
from git_plan.service.git import GitService
from git_plan.service.provider import ProviderService
from git_plan.service.providers import Provider
from git_plan.util.decorators import requires_initialized
from git_plan.util.unix import is_installed


class PlanService:
    """Manage the user's plans

    Interface:
        get_plans(branch)               -> List[Plan]
        add_plan()                      -> Plan
        import_plan(provider, issue_id) -> Plan
        edit_plan(plan)                 -> None
        delete_plan(plan)               -> None
        has_plans()                     -> bool
        get_plan_files()                -> List[Path]
        generate_next_id()              -> PlanId
    """

    def __init__(
        self,
        templates: Dict[str, str],
        git_service: GitService,
        provider_service: ProviderService,
        project: Project,
    ):
        assert "edit" in templates, "Edit template missing"
        assert "plan" in templates, "Plan template missing"
        self._plan_template = templates["plan"]
        self._edit_template = templates["edit"]
        self._git_service = git_service
        self._provider_service = provider_service
        self._project = project

    @requires_initialized
    def get_plans(self, for_branch: Optional[str] = None) -> List[Plan]:
        """Print the status of the plan

        Raises:
            RuntimeError:   Plan file not found
        """
        return self._fetch_plans(self._project, branch=for_branch)

    @requires_initialized
    def get_plan(self, with_id: str) -> Optional[Plan]:
        """Get a plan by ID

        Should load the plan from its corresponding JSON file or return None if it doesn't exist.
        """
        plan_files = self.get_plan_files()
        for file in plan_files:
            if file.stem == with_id:
                try:
                    return Plan.from_file(file, self._project)
                except ValueError:
                    return None
        return None

    @requires_initialized
    def create_plan(self) -> Plan:
        """Create a plan in the given directory

        Prompts the user to create a new plan, and then generates an ID for the plan. The ID
        is generated using the ID strategy for the current project.
        """
        provider = self._provider_service.get_local_provider()
        plan_id = self.generate_next_id(provider)
        plan = self._create_plan(self._project, plan_id)
        plan.save()
        return plan

    @requires_initialized
    def edit_plan(self, plan: Plan):
        """Update the plan in the given directory"""
        template = self._edit_template.replace("%headline%", plan.message.headline).replace(
            "%body%", plan.message.body
        )

        new_message = self._prompt_user_for_plan(initial=template)
        plan.message = new_message
        plan.updated_at = int(time.time())
        plan.save()

    @staticmethod
    def delete_plan(plan: Plan):
        """Delete the chosen plan"""
        if not plan.project.is_initialized:
            raise NotInitialized()

        if not plan.path.exists():
            raise RuntimeError(f"Plan not found: {plan}")

        plan.path.unlink()  # Deletes the file

    @requires_initialized
    def has_plans(self) -> bool:
        """Check if a plan already exists in the given directory"""
        return any(self.get_plan_files())  # False if it cannot iterate at least once

    @requires_initialized
    def get_plan_files(self) -> Iterable[Path]:
        """Returns a list of the plan files in the project

        Returns:
            An iterable of Path instances
        """
        return self._project.plan_files_dir.iterdir()

    def generate_next_id(self, provider: Optional[Provider] = None) -> PlanId:
        """Generate the next ID for the project

        Args:
            provider:   A plan provider instance

        Returns:
            An instance of PlanId, associated with the most recent plan
        """
        provider = provider or self._provider_service.get_local_provider()
        latest_plan = self._get_latest_plan()  # Optional
        return provider.generate_id(latest_plan)

    # Private #############

    def _get_latest_plan(self) -> Optional[Plan]:
        """Get the plan with the highest ID number"""
        plans = self._fetch_plans(self._project, branch=None)
        if len(plans) == 0:
            return None

        if len(plans) == 1:
            return plans[0]

        # Descending order
        return sorted(plans, key=lambda plan: plan.id.number, reverse=True)[0]

    def _create_plan(self, project: Project, plan_id: PlanId) -> Plan:
        message = self._prompt_user_for_plan()
        if not message or message.headline == "":
            raise GitPlanException("Invalid plan. Please include at least a headline.")

        branch = self._git_service.get_current_branch()
        created_at: float = time.time()
        updated_at: float = created_at
        plan = Plan(project, plan_id, branch, int(created_at), int(updated_at), message)
        plan.message = message
        return plan

    def _prompt_user_for_plan(self, initial: Optional[str] = None) -> PlanMessage:
        if not initial:
            initial = self._plan_template

        editor = self._git_service.get_configured_editor()
        if not editor:
            editor = os.environ.get("EDITOR", "vim")
        if not is_installed(editor):
            raise RuntimeError("Couldn't find an editor installed on your system.")

        with tempfile.NamedTemporaryFile(suffix=".tmp", mode="r+") as file:
            file.write(initial)
            file.flush()
            try:
                subprocess.run([editor, file.name], check=True)
            except CalledProcessError as e:
                raise GitPlanException() from e

            file.seek(0)
            with open(file.name, encoding="utf8", mode="r") as updated_file:
                message_lines = updated_file.readlines()
            processed_input = self._post_process_plan(message_lines)

            return PlanMessage.from_string(processed_input)

    def _fetch_plans(self, project: Project, branch: Optional[str] = None) -> List["Plan"]:
        """Fetch plans from disk and return them

        Args:
            project:    The current project
            branch:     Optionally filter by branch

        Returns:
            A list of plan instances
        """
        if not self.has_plans():
            return []

        plan_files = project.plan_files_dir.iterdir()
        plans: List[Plan] = []
        for file in plan_files:
            try:
                if not file.is_file():
                    continue
                plans.append(Plan.from_file(file, project))
            except ValueError:
                continue

        if branch:
            # .strip() for backwards compatibility
            plans = [plan for plan in plans if plan.branch.strip() == branch.strip()]

        return plans

    @staticmethod
    def _post_process_plan(lines: List[str]):
        lines = [line.strip() for line in lines if not line.startswith("#") or line == "\n"]
        if not lines or len(lines) == 0:
            raise PlanEmpty()

        headline = lines[0].strip()
        body = "\n".join(lines[1:]).strip()

        return "".join([headline, "\n", "\n", body])
