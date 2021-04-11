"""Project service"""

from git_plan.exceptions import AlreadyInitialized
from git_plan.model.project import Project


class ProjectService:  # pylint: disable=too-few-public-methods
    """Administrative functionality for projects"""

    @staticmethod
    def initialize(project: Project):
        """Create the plan directory"""
        if project.plan_dir.exists():
            raise AlreadyInitialized()

        project.plan_dir.mkdir()
        project.plan_files_dir.mkdir()
