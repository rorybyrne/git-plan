import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from git_plan.exceptions import NotInitialized
from git_plan.model.plan import Plan, PlanMessage
from git_plan.model.repository import Repository
from git_plan.service.git import GitService
from git_plan.service.plan import PlanService


def test_should_construct_successfully():
    git_service = GitService()
    plan_service = PlanService('.', '.', git_service)

    assert plan_service


@patch('git_plan.service.plan.PlanService._prompt_user_for_plan')
@patch.object(GitService, 'get_current_branch')
def test_add_plan_should_raise_not_initialized(mock_get_current_branch, mock_prompt_user):

    mock_prompt_user.return_value = PlanMessage('headline', 'body')
    mock_get_current_branch.return_value = 'foo_branch'

    git_service = GitService()
    plan_service = PlanService('.', '.', git_service)
    with tempfile.TemporaryDirectory() as tempdir:
        Path(tempdir, '.git').mkdir()
        project = Repository(tempdir)

        with pytest.raises(NotInitialized):
            plan_service.add_plan(project)

@patch('git_plan.service.plan.PlanService._prompt_user_for_plan')
@patch.object(GitService, 'get_current_branch')
def test_should_create_plan(mock_get_current_branch, mock_prompt_user):
    mock_prompt_user.return_value = PlanMessage('headline', 'body')
    mock_get_current_branch.return_value = 'foo_branch'

    git_service = GitService()
    plan_service = PlanService('.', '.', git_service)
    with tempfile.TemporaryDirectory() as tempdir:
        Path(tempdir, '.git').mkdir()
        Path(tempdir, '.plan').mkdir()
        Path(tempdir, '.plan', 'plans').mkdir()
        project = Repository(tempdir)

        plan = plan_service.add_plan(project)
        assert plan.message.headline == 'headline'
        assert Path(plan.path).is_file()

@patch('git_plan.service.plan.PlanService._prompt_user_for_plan')
@patch.object(GitService, 'get_current_branch')
def test_deleting_nonexistent_plan_raises_exception(mock_get_current_branch, mock_prompt_user):
    mock_prompt_user.return_value = PlanMessage('headline', 'body')
    mock_get_current_branch.return_value = 'foo_branch'

    git_service = GitService()
    plan_service = PlanService('.', '.', git_service)
    with tempfile.TemporaryDirectory() as tempdir:
        Path(tempdir, '.git').mkdir()
        Path(tempdir, '.plan').mkdir()
        Path(tempdir, '.plan', 'plans').mkdir()
        project = Repository(tempdir)

        plan = plan_service._create_plan(project, 'some_id')
        with pytest.raises(RuntimeError):
            plan_service.delete_plan(plan)
