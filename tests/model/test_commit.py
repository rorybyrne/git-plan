import json
import tempfile
from pathlib import Path

from git_plan.model.commit import Commit
from git_plan.model.project import Project

COMMIT_NO_TIME = {
    "branch": "foo",
    "message": {
        "headline": "headline",
        "body": "body"
    }
}

COMMIT_WITH_TIME = {
    "branch": "foo",
    "message": {
        "headline": "headline",
        "body": "body"
    },
    "created_at": 1616842401,
    "created_at": 1616842401,
}


def test_commit_should_auto_populate_time_fields_on_load():
    with tempfile.TemporaryDirectory() as tempdir:
        file_name = Path(tempdir, "commit-12345.txt")
        with open(file_name, 'a') as f:
            f.write(json.dumps(COMMIT_NO_TIME))

        project = Project(tempdir)
        commit = Commit.from_file(file_name, project)

        assert commit.created_at is not None, "commit missing created_at field"
        assert commit.updated_at is not None, "commit missing updated_at field"

def test_commit_should_not_auto_populate_time_fields_on_load():
    with tempfile.TemporaryDirectory() as tempdir:
        file_name = Path(tempdir, "commit-12345.txt")
        with open(file_name, 'a') as f:
            f.write(json.dumps(COMMIT_WITH_TIME))

        project = Project(tempdir)
        commit = Commit.from_file(file_name, project)

        assert commit.created_at == 1616842401, "created_at has wrong value"
        assert commit.updated_at == 1616842401, "updated_at has wrong value"
