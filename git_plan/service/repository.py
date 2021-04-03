"""Repository service"""

from git_plan.exceptions import AlreadyInitialized
from git_plan.model.repository import Repository


class RepositoryService:  # pylint: disable=too-few-public-methods
    """Administrative functionality for repositories"""

    @staticmethod
    def initialize(repo: Repository):
        """Create the plan directory"""
        if repo.plan_dir.exists():
            raise AlreadyInitialized()

        repo.plan_dir.mkdir()
        repo.plan_files_dir.mkdir()
