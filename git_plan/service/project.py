"""Project service

Author: Rory Byrne <rory@rory.bio>
"""

from git_plan.exceptions import ProjectAlreadyInitialized
from git_plan.model.project import Project


class ProjectService:  # pylint: disable=too-few-public-methods
    """Administrative functionality for projects"""

    @staticmethod
    def initialize(project: Project):
        """Create the plan directory"""
        if project.plan_dir.exists():
            raise ProjectAlreadyInitialized()

        project.plan_dir.mkdir()
