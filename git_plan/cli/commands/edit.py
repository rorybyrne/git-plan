"""Edit command

Author: Rory Byrne <rory@rory.bio>
"""
from git_plan.cli.commands.command import Command
from git_plan.model.project import Project
from git_plan.service.plan import PlanService
from git_plan.service.ui import UIService


class Edit(Command):
    """Add a new task"""

    subcommand = 'edit'

    def __init__(self, plan_service: PlanService, working_dir: str, ui_service: UIService):
        assert plan_service, "Plan service not injected"
        assert working_dir, "Working dir not injected"
        self._plan_service = plan_service
        self._ui_service = ui_service
        self._project = Project.from_working_dir(working_dir)

    def pre_command(self):
        """Perhaps some validation?"""
        pass

    def command(self):
        """Create a new task"""
        tasks = self._plan_service.get_tasks(self._project)
        if not tasks:
            print("No tasks to edit.")
            return

        chosen_task = self._ui_service.choose_task(tasks)

        self._plan_service.edit_task(chosen_task)
