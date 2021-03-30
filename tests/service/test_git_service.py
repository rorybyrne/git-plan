from subprocess import CalledProcessError
from unittest.mock import MagicMock, patch

import pytest

from git_plan.exceptions import CommitAbandoned, GitException
from git_plan.model.commit import Commit
from git_plan.service.git import GitService


class TestGitService:

    @patch('git_plan.service.git.GitService._run_command')
    def test_has_staged_files_should_return_true_on_calledprocesserror(self, run_mock: MagicMock):
        run_mock.side_effect = CalledProcessError(1, 'foo')
        git = GitService()

        assert git.has_staged_files() == True

    @patch('git_plan.service.git.GitService._run_command')
    def test_get_current_branch_should_raise_gitexception_on_failure(self, run_mock: MagicMock):
        run_mock.side_effect = CalledProcessError(1, 'foo')
        git = GitService()

        with pytest.raises(GitException):
            git.get_current_branch()

    @patch('git_plan.model.commit.Commit')
    @patch('git_plan.service.git.GitService._run_command')
    def test_commit_should_raise_commit_abandoned_on_command_failure(self, run_mock: MagicMock, commit_mock: MagicMock):
        run_mock.side_effect = CalledProcessError(1, 'foo')
        git = GitService()
        commit = MagicMock()
        commit.message = MagicMock(return_value="foo")

        with pytest.raises(CommitAbandoned):
            git.commit(commit)

    @patch('git_plan.service.git.GitService._run_command')
    def test_get_configured_editor_should_return_none_on_failure(self, run_mock: MagicMock):
        run_mock.side_effect = CalledProcessError(1, 'foo')
        git = GitService()

        assert git.get_configured_editor() == None

    @patch('git_plan.service.git.GitService._run_command')
    def test_get_configured_editor_should_return_none_on_empty_response(self, run_mock: MagicMock):
        run_mock.return_value = ""
        git = GitService()

        assert git.get_configured_editor() == None
