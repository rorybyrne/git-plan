"""Project service

Author: Rory Byrne <rory@rory.bio>
"""
import json
import os

from git_plan.model.project import Project


class ProjectService:

    def __init__(self, projects_file: str):
        assert projects_file, "Projects filename missing"
        self._projects_file = projects_file

    def load_projects(self):
        """Load the projects from the projects file"""
        try:
            with open(self._projects_file) as ph:
                plan_data = json.load(ph)

            return plan_data['plans']
        except FileNotFoundError:
            print("Couldn't find plans file")
            return []

    @staticmethod
    def initialize(project: Project):
        plan_dir = project.plan_dir
        if os.path.exists(plan_dir):
            print("Project already initialized.")
            return

        os.mkdir(plan_dir)
