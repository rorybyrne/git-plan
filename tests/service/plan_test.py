import json
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from git_plan.exceptions import ConfigurationError, NotInitialized
from git_plan.model.plan import Plan, PlanId, PlanMessage
from git_plan.model.project import Project
from git_plan.service.git import GitService
from git_plan.service.plan import PlanService
from git_plan.service.provider import ProviderService

provider_service = ProviderService("TST")
git_service = GitService()


class TestPlanService:

    @pytest.fixture
    def plan_service(self) -> PlanService:
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

        try:
            yield plan_service
        finally:
            tempdir.cleanup()



    def test_should_construct_successfully(self, plan_service):
        assert plan_service


    @patch('git_plan.service.plan.PlanService._prompt_user_for_plan')
    @patch.object(GitService, 'get_current_branch')
    def test_add_plan_should_raise_not_initialized(self, mock_get_current_branch, mock_prompt_user):

        mock_prompt_user.return_value = PlanMessage('headline', 'body')
        mock_get_current_branch.return_value = 'foo_branch'
        templates = {
            "plan": "",
            "edit": ""
        }
        plan_service = PlanService(templates, git_service, provider_service, Project("foo"))

        with pytest.raises(NotInitialized):
            plan_service.add_plan()


    @patch('git_plan.service.plan.PlanService._prompt_user_for_plan')
    @patch.object(GitService, 'get_current_branch')
    def test_should_create_plan(self, mock_get_current_branch, mock_prompt_user, plan_service):
        mock_prompt_user.return_value = PlanMessage('headline', 'body')
        mock_get_current_branch.return_value = 'foo_branch'

        plan = plan_service.add_plan()
        assert plan.message.headline == 'headline'
        assert Path(plan.path).is_file()


    @patch('git_plan.service.plan.PlanService._prompt_user_for_plan')
    @patch.object(GitService, 'get_current_branch')
    def test_deleting_nonexistent_plan_raises_exception(
        self, mock_get_current_branch, mock_prompt_user, plan_service: PlanService
    ):
        mock_prompt_user.return_value = PlanMessage('headline', 'body')
        mock_get_current_branch.return_value = 'foo_branch'

        plan_id = PlanId("TST", 41)
        plan = plan_service._create_plan(plan_service._project, plan_id)
        with pytest.raises(RuntimeError):
            plan_service.delete_plan(plan)


    @patch('git_plan.service.plan.PlanService._get_latest_plan')
    def test_generate_next_id_should_increment_number_only(self, mock_get_latest, plan_service):
        plan_id = PlanId("TST", 41)
        plan = Plan(None, plan_id, None, None, None)
        mock_get_latest.return_value = plan

        provider = provider_service.get_local_provider()
        new_id = plan_service.generate_next_id(provider)

        assert new_id.number == 42


    @patch('git_plan.service.plan.PlanService._get_latest_plan')
    def test_generate_next_id_should_choose_1_if_no_latest_plan(self, mock_get_latest, plan_service):
        mock_get_latest.return_value = None

        provider = provider_service.get_local_provider()
        new_id = plan_service.generate_next_id(provider)

        assert new_id.number == 1


    @patch('git_plan.service.plan.PlanService._get_latest_plan')
    def test_generate_next_id_should_raise_if_label_does_not_match(self, mock_get_latest, plan_service):
        plan_id = PlanId("FOO", 41)
        plan = Plan(None, plan_id, None, None, None)
        mock_get_latest.return_value = plan

        provider = provider_service.get_local_provider()
        with pytest.raises(ConfigurationError):
            plan_service.generate_next_id(provider)
