import tempfile
from pathlib import Path

import pytest

from git_plan.exceptions import NotAGitRepository, AlreadyInitialized
from git_plan.model.repository import Repository
from git_plan.service.repository import RepositoryService


class TestProjectService:

    def test_initialize_should_succeed_in_a_fresh_git_repository(self):
        with tempfile.TemporaryDirectory() as tempdir:
            Path(tempdir, '.git').mkdir()
            svc = RepositoryService()
            project = Repository(tempdir)

            svc.initialize(project)

    def test_initialize_should_succeed_in_a_non_git_repository(self):
        with tempfile.TemporaryDirectory() as tempdir:
            svc = RepositoryService()
            project = Repository(tempdir)

            svc.initialize(project)

    def test_initialize_should_raise_alreadyinitialized_if_run_twice(self):
        with tempfile.TemporaryDirectory() as tempdir:
            Path(tempdir, '.git').mkdir()
            svc = RepositoryService()
            project = Repository(tempdir)

            svc.initialize(project)
            with pytest.raises(AlreadyInitialized):
                svc.initialize(project)
