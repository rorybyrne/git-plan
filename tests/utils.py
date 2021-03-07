import os
from pathlib import Path
from random import randint

from git_plan.service.git import GitService
from git_plan.service.plan import PlanService

ROOT_PATH = os.path.join(Path.home(), '.cache', 'git_plan')


def create_test_project():
    rn = randint(1, 100000)
    test_dir = os.path.join(ROOT_PATH, f'test-{rn}')

    os.makedirs(os.path.join(test_dir, '.git'), exist_ok=True)

    return test_dir


def construct_plan_service(plan_home=None, edit_template_file: str = None, commit_template_file: str = None) -> PlanService:
    if not plan_home:
        rn = randint(1, 100000)
        plan_home = os.path.join(ROOT_PATH, f'plan_home-{rn}')
    if not edit_template_file:
        edit_template_file = os.path.join(plan_home, 'edit')
    if not commit_template_file:
        commit_template_file = os.path.join(plan_home, 'commit')

    git_service = GitService()

    return PlanService(plan_home, commit_template_file, git_service, edit_template_file)
