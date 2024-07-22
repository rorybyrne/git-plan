"""Project service"""

from pathlib import Path

from git_plan.constants import GP_DIR, GP_PLANS_SUBDIR, GP_PROJECT_FNAME
from git_plan.exceptions import AlreadyInitialized, NotAGitRepository
from git_plan.model.project import Project
from git_plan.util import git


class ProjectService:  # pylint: disable=too-few-public-methods
    """Administrative functionality for projects"""

    @staticmethod
    def initialize(root_dir: Path) -> Project:
        """Create the plan directory"""
        if not git.is_git_repository(root_dir):
            raise NotAGitRepository()
        plan_dir = root_dir / GP_DIR
        if plan_dir.exists():
            raise AlreadyInitialized()

        plan_dir.mkdir()
        plan_files_dir = plan_dir / GP_PLANS_SUBDIR
        plan_files_dir.mkdir()

        project = Project(root_dir)
        project.save(root_dir / GP_DIR / GP_PROJECT_FNAME)

        return project
