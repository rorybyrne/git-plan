"""Project service

Author: Rory Byrne <rory@rory.bio>
"""
from git_plan.exceptions import NotAGitRepository
from git_plan.util.git import get_repository_root
import os

from git_plan.model.project import Project


class ProjectService:

    @staticmethod
    def has_commits(project: Project):
        return os.listdir(project.plan_dir)

    @staticmethod
    def initialize(project: Project):
        plan_dir = project.plan_dir
        if os.path.exists(plan_dir):
            return

        os.mkdir(plan_dir)
