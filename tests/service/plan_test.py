import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from git_plan.exceptions import ConfigurationError, NotInitialized
from git_plan.model.plan import Plan, PlanId, PlanMessage
from git_plan.model.project import Project
from git_plan.service.git import GitService
from git_plan.service.plan import PlanService
from git_plan.service.provider import ProviderService

provider_service = ProviderService("TST")
git_service = GitService()


def test_should_construct_successfully():
    git_service = GitService()
    plan_service = PlanService('.', '.', git_service, provider_service, Project("foo"))

    assert plan_service


@patch('git_plan.service.plan.PlanService._prompt_user_for_plan')
@patch.object(GitService, 'get_current_branch')
def test_add_plan_should_raise_not_initialized(mock_get_current_branch, mock_prompt_user):

    mock_prompt_user.return_value = PlanMessage('headline', 'body')
    mock_get_current_branch.return_value = 'foo_branch'

    with tempfile.TemporaryDirectory() as tempdir:
        Path(tempdir, '.git').mkdir()
        project = Project(tempdir)
        plan_service = PlanService('.', '.', git_service, provider_service, project)

        with pytest.raises(NotInitialized):
            plan_service.add_plan()


@patch('git_plan.service.plan.PlanService._prompt_user_for_plan')
@patch.object(GitService, 'get_current_branch')
def test_should_create_plan(mock_get_current_branch, mock_prompt_user):
    mock_prompt_user.return_value = PlanMessage('headline', 'body')
    mock_get_current_branch.return_value = 'foo_branch'

    with tempfile.TemporaryDirectory() as tempdir:
        Path(tempdir, '.git').mkdir()
        Path(tempdir, '.plan').mkdir()
        Path(tempdir, '.plan', 'plans').mkdir()
        project = Project(tempdir)
        plan_service = PlanService('.', '.', git_service, provider_service, project)

        plan = plan_service.add_plan()
        assert plan.message.headline == 'headline'
        assert Path(plan.path).is_file()


@patch('git_plan.service.plan.PlanService._prompt_user_for_plan')
@patch.object(GitService, 'get_current_branch')
def test_deleting_nonexistent_plan_raises_exception(mock_get_current_branch, mock_prompt_user):
    mock_prompt_user.return_value = PlanMessage('headline', 'body')
    mock_get_current_branch.return_value = 'foo_branch'

    with tempfile.TemporaryDirectory() as tempdir:
        Path(tempdir, '.git').mkdir()
        Path(tempdir, '.plan').mkdir()
        Path(tempdir, '.plan', 'plans').mkdir()
        repo = Project(tempdir)
        plan_service = PlanService('.', '.', git_service, provider_service, repo)

        plan = plan_service._create_plan(repo, 'some_id')
        with pytest.raises(RuntimeError):
            plan_service.delete_plan(plan)


@patch('git_plan.service.plan.PlanService._get_latest_plan')
def test_generate_next_id_should_increment_number_only(mock_get_latest):
    plan_id = PlanId("TST", 41)
    plan = Plan(None, plan_id, None, None, None)
    mock_get_latest.return_value = plan

    plan_service = PlanService('.', '.', git_service, provider_service, Project('foo'))
    provider = provider_service.get_local_provider()
    new_id = plan_service._generate_next_id(provider)

    assert new_id.number == 42


@patch('git_plan.service.plan.PlanService._get_latest_plan')
def test_generate_next_id_should_choose_1_if_no_latest_plan(mock_get_latest):
    mock_get_latest.return_value = None

    plan_service = PlanService('.', '.', git_service, provider_service, Project('foo'))
    provider = provider_service.get_local_provider()
    new_id = plan_service._generate_next_id(provider)

    assert new_id.number == 1


@patch('git_plan.service.plan.PlanService._get_latest_plan')
def test_generate_next_id_should_raise_if_label_does_not_match(mock_get_latest):
    plan_id = PlanId("FOO", 41)
    plan = Plan(None, plan_id, None, None, None)
    mock_get_latest.return_value = plan

    plan_service = PlanService('.', '.', git_service, provider_service, Project('foo'))
    provider = provider_service.get_local_provider()
    with pytest.raises(ConfigurationError):
        plan_service._generate_next_id(provider)
