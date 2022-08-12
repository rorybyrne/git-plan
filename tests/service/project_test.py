import tempfile
from pathlib import Path

import pytest

from git_plan.exceptions import AlreadyInitialized
from git_plan.model.project import Project
from git_plan.service.project import ProjectService


class TestProjectService:

    def test_initialize_should_succeed_in_a_fresh_git_repository(self):
        with tempfile.TemporaryDirectory() as tempdir:
            Path(tempdir, '.git').mkdir()
            svc = ProjectService()
            project = Project(tempdir)

            svc.initialize(project)

    def test_initialize_should_succeed_in_a_non_git_repository(self):
        with tempfile.TemporaryDirectory() as tempdir:
            svc = ProjectService()
            project = Project(tempdir)

            svc.initialize(project)

    def test_initialize_should_raise_alreadyinitialized_if_run_twice(self):
        with tempfile.TemporaryDirectory() as tempdir:
            Path(tempdir, '.git').mkdir()
            svc = ProjectService()
            project = Project(tempdir)

            svc.initialize(project)
            with pytest.raises(AlreadyInitialized):
                svc.initialize(project)
