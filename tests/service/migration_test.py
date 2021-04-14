import json
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from git_plan.model.plan import Plan, PlanId, PlanMessage
from git_plan.model.project import Project
from git_plan.service.git import GitService
from git_plan.service.migration import MigrationService
from git_plan.service.plan import PlanService
from git_plan.service.provider import ProviderService

OLD_FORMAT_PLAN = {
    "branch": "foo",
    "message": {
        "headline": "headline",
        "body": "body",
    },
    "created_at": 12345,
    "updated_at": 67890
}


class TestMigrationService:

    @pytest.fixture
    def migration_service(self):
        provider_service = ProviderService("TST")
        git_service = GitService()
        tempdir = tempfile.TemporaryDirectory()
        Path(tempdir.name, '.git').mkdir()
        Path(tempdir.name, '.plan').mkdir()
        Path(tempdir.name, '.plan', 'plans').mkdir()
        project = Project(Path(tempdir.name))
        templates = {
            "plan": "",
            "edit": ""
        }
        plan_service = PlanService(templates, git_service, provider_service, project)
        migration_service = MigrationService(plan_service, project)

        try:
            yield migration_service
        finally:
            tempdir.cleanup()

    @patch('git_plan.service.plan.PlanService._get_latest_plan')
    def test_perform_migration_should_add_an_id_field_to_the_json_data(
        self, mock_get_latest, migration_service: MigrationService
    ):
        plan_id = PlanId("TST", 41)
        plan = Plan(migration_service._plan_service._project, plan_id, "branch", 12345, 12345)
        mock_get_latest.return_value = plan

        file = migration_service._plan_service._project.plan_files_dir / 'commit-12345.txt'
        with open(file, 'a') as fp:
            json.dump(OLD_FORMAT_PLAN, fp)

        migration_service.migrate()

        with open(file.with_name("TST-42")) as fp:
            data = json.load(fp)
            assert "id" in data and data["id"] == "TST-42"

    @patch('git_plan.service.plan.PlanService._get_latest_plan')
    def test_perform_migration_should_not_run_twice(self, mock_get_latest, migration_service: MigrationService):
        plan_id = PlanId("TST", 41)
        plan = Plan(migration_service._plan_service._project, plan_id, "branch", 12345, 12345)
        mock_get_latest.return_value = plan

        file = migration_service._plan_service._project.plan_files_dir / 'commit-12345.txt'
        with open(file, 'a') as fp:
            json.dump(OLD_FORMAT_PLAN, fp)

        migration_service.migrate()
        migration_service._perform_migration = MagicMock()

        migration_service.migrate()
        migration_service._perform_migration.assert_not_called()
