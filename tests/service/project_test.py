import tempfile
from pathlib import Path

import pytest

from git_plan.exceptions import AlreadyInitialized, NotAGitRepository
from git_plan.model.project import Project
from git_plan.service.project import ProjectService


class TestProjectService:

    def test_initialize_should_succeed_in_a_fresh_git_repository(self, project: Project):
        pass

    def test_initialize_should_succeed_in_a_non_git_repository(self):
        with tempfile.TemporaryDirectory() as tempdir:
            with pytest.raises(NotAGitRepository):
                ProjectService.initialize(Path(tempdir))

    def test_initialize_should_raise_alreadyinitialized_if_run_twice(self):
        with tempfile.TemporaryDirectory() as tempdir:
            Path(tempdir, ".git").mkdir()
            ProjectService.initialize(Path(tempdir))
            with pytest.raises(AlreadyInitialized):
                ProjectService.initialize(Path(tempdir))
