"""Commit model

Author: Rory Byrne <rory@rory.bio>
"""
import json
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
                commit_data = json.load(f)

            return CommitMessage(**commit_data['message'])
        except Exception as e:
            print(e)
            raise RuntimeError(f'Failed to load commit from disk: {path}')

    @classmethod
    def from_string(cls, string: str):
        components = string.split('\n\n')
        if len(components) == 2:
            return CommitMessage(components[0], components[1])
        elif len(components) > 2:
            return CommitMessage(components[0], '\n\n'.join(components[1:]))
        else:
            raise RuntimeError(f'Could not parse commit message from string: "{string}"')


@dataclass
class Commit:
    project: Project
    id: str
    branch: str
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

        commit_dict = {
            "branch": self.branch,
            'message': {
                "headline": self.message.headline,
                "body": self.message.body
            },
        }

        with open(self.path, 'w') as f:
            f.write(json.dumps(commit_dict))

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
        with open(full_path, 'r') as f:
            commit_data = json.load(f)

        commit_message = CommitMessage(**commit_data['message'])
        commit_id = filename.split('.')[0].split('-')[1]
        branch = commit_data['branch']
        commit = Commit(project, commit_id, branch)
        commit.message = commit_message

        return commit

    def __str__(self):
        if not self._message:
            return super().__str__()
        return self._message.__str__()
