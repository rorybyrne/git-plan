import os
import tempfile
from unittest.mock import patch

from git_plan.model.commit import CommitMessage
from git_plan.model.project import Project
from git_plan.service.git import GitService
from git_plan.service.plan import PlanService


def test_should_construct_successfully():
    git_service = GitService()
    plan_service = PlanService('.', '.', git_service)

    assert plan_service


@patch('git_plan.service.plan.PlanService._prompt_user_for_plan')
@patch.object(GitService, 'get_current_branch')
def test_should_create_commit(mock_get_current_branch, mock_prompt_user):

    mock_prompt_user.return_value = CommitMessage('headline', 'body')
    mock_get_current_branch.return_value = 'foo_branch'

    git_service = GitService()
    plan_service = PlanService('.', '.', git_service)
    with tempfile.TemporaryDirectory() as tempdir:
        os.mkdir(os.path.join(tempdir, '.git'))
        project = Project(tempdir)

        commit = plan_service._create_commit(project, 'foo')
        assert commit.message.headline == 'headline'
