"""Plan service

@author Rory Byrne <rory@rory.bio>
"""
import json
import os
import tempfile
import time
from subprocess import call
from typing import List

from git_plan.model.project import Project
from git_plan.model.task import Task


class PlanService:

    PROJECTS_FILE = 'projects.json'
    TASK_FILE_TEMPLATE = 'task-{timestamp}'

    def create_task(self, project: Project):
        """Create a plan in the given directory

        1. Create a new file in .git/ containing the plan
        """
        content = self._plan_task()
        task_id = str(int(time.time()))
        task = Task(project, task_id)
        task.content = content
        task.save()

    def update_task(self, task: Task, new_content: str):
        """Update the plan in the given directory"""
        pass

    def delete_task(self, task: Task):
        pass

    @staticmethod
    def has_tasks(project: Project) -> bool:
        """Check if a plan already exists in the given directory"""
        return project.has_tasks()

    @staticmethod
    def get_tasks(project: Project) -> List[Task]:
        """Print the status of the plan

        Raises:
            RuntimeError:   Task file not found
        """
        return Task.fetch_tasks(project)

    def load_plans(self, plan_home: str):
        """Returns a list of directories"""
        try:
            plans_file = os.path.join(plan_home, self.PROJECTS_FILE)
            with open(plans_file) as ph:
                plan_data = json.load(ph)

            return plan_data['plans']
        except FileNotFoundError:
            print("Couldn't find plans file")
            return []

    # Private #############

    @staticmethod
    def _plan_task(initial: str = ''):
        editor = os.environ.get('EDITOR', 'vim')

        with tempfile.NamedTemporaryFile(suffix=".tmp", mode='r+') as tf:
            tf.write(initial)
            tf.flush()
            call([editor, tf.name])

            tf.seek(0)
            edited_message = tf.read()

            return edited_message
