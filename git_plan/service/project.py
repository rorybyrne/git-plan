"""Project service

Author: Rory Byrne <rory@rory.bio>
"""

from git_plan.exceptions import NotAGitRepository, ProjectAlreadyInitialized
from git_plan.model.project import Project


class ProjectService:  # pylint: disable=too-few-public-methods
    """Administrative functionality for projects"""

    @staticmethod
    def initialize(project: Project):
        """Create the plan directory"""
        if project.plan_dir.exists():
            raise ProjectAlreadyInitialized()

        if not project.is_git_repository():
            raise NotAGitRepository()

        project.plan_dir.mkdir()
        project.plan_files_dir.mkdir()
