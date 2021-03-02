"""Task model

Author: Rory Byrne <rory@rory.bio>
"""
import os
from dataclasses import dataclass, field
from typing import List

from git_plan.model.project import Project


@dataclass
class TaskContent:
    headline: str
    body: str

    def __str__(self):
        return f'''{self.headline}
        
{self.body}
        '''

    @classmethod
    def from_file(cls, path: str):
        """Load a Task's content from a file"""
        try:
            with open(path, 'r') as f:
                headline = f.readline().strip()
                f.readline()
                body = f.read().strip()

                return TaskContent(headline, body)
        except Exception as e:
            print(e)
            raise RuntimeError(f'Failed to load task from disk: {path}')

    @classmethod
    def from_string(cls, string: str):
        components = string.split('\n\n')
        if len(components) != 2:
            raise RuntimeError(f'Could not parse task contents from string: "{string}"')

        return TaskContent(components[0], components[1])


@dataclass
class Task:
    project: Project
    id: str
    _content: TaskContent = field(init=False, default=None)

    EXT = '.txt'

    @property
    def filename(self):
        return f'task-{self.id}'

    @property
    def path(self):
        local_plan_dir = '.git/plan'
        return os.path.join(self.project.root_dir, local_plan_dir, self.filename + self.EXT)

    @property
    def content(self):
        if not self._content:
            try:
                self.content = TaskContent.from_file(self.path)
            except RuntimeError as e:
                print(e)
                raise RuntimeError(f"Task doesn't exist at location: {self.path}")

        return self._content

    @content.setter
    def content(self, value: TaskContent):
        self._content = value

    def save(self):
        """Persist the task to the storage"""
        if not self._content:
            raise RuntimeError("Cannot save a task with no content.")

        # Create plan/ directory if needed
        os.makedirs(os.path.dirname(self.path), exist_ok=True)

        with open(self.path, 'w') as f:
            f.write(str(self.content))

    @classmethod
    def fetch_tasks(cls, project: Project) -> List['Task']:
        if not project.has_tasks():
            return []

        task_files = os.listdir(project.plan_dir)
        tasks = [cls.from_file(f, project) for f in task_files]

        return tasks

    @classmethod
    def from_file(cls, filename: str, project: Project):
        """Load a task from a file"""
        full_path = os.path.join(project.plan_dir, filename)
        task_content = TaskContent.from_file(full_path)
        task_id = filename.split('.')[0].split('-')[1]
        task = Task(project, task_id)
        task.content = task_content

        return task

    def __str__(self):
        if not self._content:
            return super().__str__()
        return self._content.__str__()
