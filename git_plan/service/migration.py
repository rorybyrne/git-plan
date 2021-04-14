"""Migration service"""
import json
import shutil
from pathlib import Path

from git_plan.model.project import Project
from git_plan.service.plan import PlanService
from git_plan.util.decorators import requires_initialized


class MigrationService:
    """Functionality for migrating plan data from old formats to new

    Interface:
        backup()                -> None
        should_migrate()        -> bool
        migrate()               -> None
    """

    def __init__(self, plan_service: PlanService, project: Project):
        self._plan_service = plan_service
        self._project = project

    @requires_initialized
    def backup(self):
        """Backup the .plan directory"""
        directory = self._project.plan_dir
        self._copy_and_overwrite(directory, directory.with_suffix('.bkp'))

    @requires_initialized
    def should_migrate(self) -> bool:
        """Checks whether any plans exist with the old formatting"""
        plan_files = self._plan_service.get_plan_files()
        return any(self._should_migrate(plan_file) for plan_file in plan_files)

    @requires_initialized
    def migrate(self):
        """Migrates plan files to the new format"""
        plan_files = self._plan_service.get_plan_files()
        plan_files = sorted(plan_files, key=lambda filename: int(filename.stem.split('-')[1]))
        for plan_file in plan_files:
            if self._should_migrate(plan_file):
                self._perform_migration(plan_file)

    # Private ###################################

    @staticmethod
    def _copy_and_overwrite(from_path: Path, to_path: Path):
        """Copy a directory to a new location, overwriting if it already exists

        Args:
            from_path:      A Path location to copy from
            to_path:        A Path location to copy to
        """
        if to_path.exists():
            shutil.rmtree(to_path)

        shutil.copytree(from_path, to_path)

    def _perform_migration(self, plan_file: Path):
        """Migrate the data in the plan file

        Args:
            plan_file:  The plan file to migrate
        """
        if not self._should_migrate(plan_file):
            print(f"Error: tried to migrate plan file which should not be migrated: {plan_file}")
            return

        next_id = self._plan_service.generate_next_id()
        with open(plan_file) as fp:
            data = json.load(fp)

        # Write to GP-1, instead of commit-12345
        with open(plan_file.with_name(str(next_id)), 'w') as fp:
            data["id"] = str(next_id)
            json.dump(data, fp)
            plan_file.unlink()

    @staticmethod
    def _should_migrate(plan_file: Path) -> bool:
        """Returns true if the plan file needs to be migrated to the new format"""
        with open(plan_file) as fp:
            data = json.load(fp)

        return "id" not in data
