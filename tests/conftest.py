import tempfile
from pathlib import Path

import pytest

from git_plan.constants import GIT_DIR
from git_plan.service.project import ProjectService


@pytest.fixture
def tempdir():
    with tempfile.TemporaryDirectory() as some_dir:
        yield Path(some_dir)


@pytest.fixture
def project(tempdir: Path):
    (tempdir / GIT_DIR).mkdir()  # mock git
    _project = ProjectService.initialize(tempdir)
    yield _project
