import json
import tempfile
from pathlib import Path

from git_plan.model.plan import Plan
from git_plan.model.repository import Repository

PLAN_NO_TIME = {
    "branch": "foo",
    "message": {
        "headline": "headline",
        "body": "body"
    }
}

PLAN_WITH_TIME = {
    "branch": "foo",
    "message": {
        "headline": "headline",
        "body": "body"
    },
    "created_at": 1616842401,
    "created_at": 1616842401,
}


def test_plan_should_auto_populate_time_fields_on_load():
    with tempfile.TemporaryDirectory() as tempdir:
        file_name = Path(tempdir, "commit-12345.txt")
        with open(file_name, 'a') as f:
            f.write(json.dumps(PLAN_NO_TIME))

        project = Repository(tempdir)
        plan = Plan.from_file(file_name, project)

        assert plan.created_at is not None, "plan missing created_at field"
        assert plan.updated_at is not None, "plan missing updated_at field"

def test_plan_should_not_auto_populate_time_fields_on_load():
    with tempfile.TemporaryDirectory() as tempdir:
        file_name = Path(tempdir, "commit-12345.txt")
        with open(file_name, 'a') as f:
            f.write(json.dumps(PLAN_WITH_TIME))

        project = Repository(tempdir)
        plan = Plan.from_file(file_name, project)

        assert plan.created_at == 1616842401, "created_at has wrong value"
        assert plan.updated_at == 1616842401, "updated_at has wrong value"
