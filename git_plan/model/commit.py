"""Commit model

Author: Rory Byrne <rory@rory.bio>
"""
import os
from dataclasses import dataclass, field
from typing import List

from git_plan.model.project import Project


@dataclass
class CommitMessage:
    headline: str
    body: str

    def __str__(self):
        return f'''{self.headline}

{self.body}
        '''

    @classmethod
    def from_file(cls, path: str):
        """Load a commit's message from a file"""
        try:
            with open(path, 'r') as f:
                headline = f.readline().strip()
                f.readline()
                body = f.read().strip()

                return CommitMessage(headline, body)
        except Exception as e:
            print(e)
            raise RuntimeError(f'Failed to load commit from disk: {path}')

    @classmethod
    def from_string(cls, string: str):
        components = string.split('\n\n')
        if len(components) != 2:
            raise RuntimeError(f'Could not parse commit message from string: "{string}"')

        return CommitMessage(components[0], components[1])


@dataclass
class Commit:
    project: Project
    id: str
    branch: str = 'gh-11/pretty-list'
    _message: CommitMessage = field(init=False, default=None)

    EXT = '.txt'

    @property
    def filename(self):
        return f'commit-{self.id}'

    @property
    def path(self):
        local_plan_dir = '.git/plan'
        return os.path.join(self.project.root_dir, local_plan_dir, self.filename + self.EXT)

    @property
    def message(self):
        if not self._message:
            try:
                self.message = CommitMessage.from_file(self.path)
            except RuntimeError as e:
                print(e)
                raise RuntimeError(f"Commit doesn't exist at location: {self.path}")

        return self._message

    @message.setter
    def message(self, value: CommitMessage):
        self._message = value

    def save(self):
        """Persist the commit to the storage"""
        if not self._message:
            raise RuntimeError("Cannot save a commit with no message.")

        # Create plan/ directory if needed
        os.makedirs(os.path.dirname(self.path), exist_ok=True)

        with open(self.path, 'w') as f:
            f.write(str(self.message))

    @classmethod
    def fetch_commits(cls, project: Project) -> List['Commit']:
        if not project.has_commits():
            return []

        commit_files = os.listdir(project.plan_dir)
        commits = [cls.from_file(f, project) for f in commit_files]

        return commits

    @classmethod
    def from_file(cls, filename: str, project: Project):
        """Load a commit from a file"""
        full_path = os.path.join(project.plan_dir, filename)
        commit_message = CommitMessage.from_file(full_path)
        commit_id = filename.split('.')[0].split('-')[1]
        commit = Commit(project, commit_id)
        commit.message = commit_message

        return commit

    def __str__(self):
        if not self._message:
            return super().__str__()
        return self._message.__str__()
