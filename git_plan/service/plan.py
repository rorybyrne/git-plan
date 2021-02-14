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
from git_plan.model.task import Task, TaskContent


class PlanService:

    def __init__(self, plan_home: str, task_template_file: str, projects_file: str):
        assert task_template_file, "Task template filename missing"
        assert projects_file, "Projects filename missing"
        self._task_template_file = os.path.join(plan_home, task_template_file)
        self._projects_file = os.path.join(plan_home, projects_file)
        self._plan_home = plan_home

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
        """Delete the chosen task"""
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

    def load_plans(self):
        """Returns a list of directories"""
        try:
            with open(self._projects_file) as ph:
                plan_data = json.load(ph)

            return plan_data['plans']
        except FileNotFoundError:
            print("Couldn't find plans file")
            return []

    # Private #############

    def _plan_task(self, initial: str = None) -> TaskContent:
        editor = os.environ.get('EDITOR', 'vim')
        if not initial:
            with open(self._task_template_file, 'r') as f:
                initial = f.read()

        with tempfile.NamedTemporaryFile(suffix=".tmp", mode='r+') as tf:
            tf.write(initial)
            tf.flush()
            call([editor, tf.name])

            tf.seek(0)
            message_lines = tf.readlines()
            processed_input = self._post_process_task(message_lines)

            return TaskContent.from_string(processed_input)

    def _post_process_task(self, lines: List[str]):
        lines = [line.strip() for line in lines if not line.startswith('#') or line == '\n']
        headline = lines[0].strip()
        body = '\n'.join(lines[1:]).strip()

        return ''.join([headline, '\n', '\n', body])
