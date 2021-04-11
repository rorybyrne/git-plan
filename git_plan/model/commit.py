"""Commit model

Author: Rory Byrne <rory@rory.bio>
"""
import json
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from git_plan.exceptions import GitPlanException, NotInitialized
from git_plan.model.repository import Repository

COMMIT_FILE_EXT = '.txt'


@dataclass
class CommitMessage:
    """The message of a commit"""
    headline: str
    body: str

    def __str__(self):
        return f'''{self.headline}

{self.body}
        '''

    @classmethod
    def from_file(cls, path: Path):
        """Load a commit's message from a file"""
        try:
            with open(path, 'r') as file:
                commit_data = json.load(file)

            return CommitMessage(**commit_data['message'])
        except Exception as exc:
            raise GitPlanException(f'Failed to load commit from disk: {path}') from exc

    @classmethod
    def from_string(cls, string: str):
        """Construct a CommitMessage from a well-formatted string"""
        components = string.split('\n\n')
        if len(components) == 2:
            return CommitMessage(components[0], components[1])

        if len(components) > 2:
            return CommitMessage(components[0], '\n\n'.join(components[1:]))

        raise GitPlanException(f'Could not parse commit message from string: "{string}"')


@dataclass
class Commit:
    """Represents a planned commit"""
    repository: Repository
    id: str
    branch: str
    created_at: int
    updated_at: int
    _message: Optional[CommitMessage] = field(init=False, default=None)

    @property
    def filename(self):
        """The filename where this plan is stored"""
        return f'commit-{self.id}'

    @property
    def path(self) -> Path:
        """The absolute path where this plan is stored"""
        return Path(self.repository.plan_files_dir / self.filename).with_suffix(COMMIT_FILE_EXT).resolve()

    @property
    def message(self):
        """Returns the commit message, loading it from disk if needed"""
        if not self._message:
            try:
                self.message = CommitMessage.from_file(self.path)
            except RuntimeError as exc:
                raise RuntimeError(f"Commit doesn't exist at location: {self.path}") from exc

        return self._message

    @message.setter
    def message(self, value: CommitMessage):
        self._message = value

    def save(self):
        """Persist the commit to the storage"""
        if not self._message:
            raise RuntimeError("Cannot save a commit with no message.")

        if not self.repository.is_initialized():
            raise NotInitialized()

        if not self.created_at:
            raise ValueError("Missing created_at")

        if not self.created_at:
            raise ValueError("Missing updated_at")

        commit_dict = {
            "branch": self.branch.strip(),
            'message': {
                "headline": self.message.headline.strip(),
                "body": self.message.body.strip()
            },
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

        with open(self.path, 'w') as file:
            file.write(json.dumps(commit_dict))

    @classmethod
    def from_file(cls, file: Path, repository: Repository) -> "Commit":
        """Load a commit from a file"""
        with open(file, 'r') as fp:
            commit_data = json.load(fp)

        commit_message = CommitMessage(**commit_data['message'])
        commit_id = file.stem.split('-')[1]
        branch = commit_data['branch']
        created_at = commit_data.get('created_at', time.time())
        updated_at = commit_data.get('updated_at', created_at)

        commit = Commit(
            repository,
            commit_id,
            branch,
            int(created_at),
            int(updated_at)
        )
        commit.message = commit_message

        return commit

    def __str__(self):
        if not self._message:
            return super().__str__()
        return self._message.__str__()
