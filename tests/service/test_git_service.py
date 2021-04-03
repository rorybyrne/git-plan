from subprocess import CalledProcessError
from unittest.mock import MagicMock, patch

import pytest

from git_plan.exceptions import CommitAbandoned, GitException
from git_plan.model.commit import Commit
from git_plan.service.git import GitService


class TestGitService:

    @patch('git_plan.util.unix.run_command')
    @patch('git_plan.util.decorators._shell_is_in_git_repository')
    def test_has_staged_files_should_return_true_on_calledprocesserror(
            self,
            is_git_mock: MagicMock,
            run_mock: MagicMock
    ):
        is_git_mock.return_value = True
        run_mock.side_effect = CalledProcessError(1, 'foo')
        git = GitService()

        assert git.has_staged_files()

    @patch('git_plan.util.unix.run_command')
    @patch('git_plan.util.decorators._shell_is_in_git_repository')
    def test_get_current_branch_should_raise_gitexception_on_failure(
            self,
            is_git_mock: MagicMock,
            run_mock: MagicMock
    ):
        is_git_mock.return_value = True
        run_mock.side_effect = CalledProcessError(1, 'foo')
        git = GitService()

        with pytest.raises(GitException):
            git.get_current_branch()

    @patch('git_plan.model.commit.Commit')
    @patch('git_plan.util.unix.run_command')
    @patch('git_plan.util.decorators._shell_is_in_git_repository')
    def test_commit_should_raise_commit_abandoned_on_command_failure(
            self,
            is_git_mock: MagicMock,
            run_mock: MagicMock,
            commit_mock: MagicMock
    ):
        is_git_mock.return_value = True
        run_mock.side_effect = CalledProcessError(1, 'foo')
        git = GitService()
        commit = MagicMock()
        commit.message = MagicMock(return_value="foo")

        with pytest.raises(CommitAbandoned):
            git.commit(commit)

    @patch('git_plan.util.unix.run_command')
    @patch('git_plan.util.decorators._shell_is_in_git_repository')
    def test_get_configured_editor_should_return_none_on_failure(self, is_git_mock: MagicMock, run_mock: MagicMock):
        is_git_mock.return_value = True
        run_mock.side_effect = CalledProcessError(1, 'foo')
        git = GitService()

        assert git.get_configured_editor() is None

    @patch('git_plan.util.unix.run_command')
    @patch('git_plan.util.decorators._shell_is_in_git_repository')
    def test_get_configured_editor_should_return_none_on_empty_response(
            self,
            is_git_mock: MagicMock,
            run_mock: MagicMock
    ):
        is_git_mock.return_value = True
        run_mock.return_value = ""
        git = GitService()

        assert git.get_configured_editor() is None
