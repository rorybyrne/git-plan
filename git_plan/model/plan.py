"""Plan model

Author: Rory Byrne <rory@rory.bio>
"""
import json
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from git_plan.exceptions import GitPlanException, NotInitialized
from git_plan.model.project import Project

PLAN_FILE_EXT = '.txt'


@dataclass
class PlanMessage:
    """The message of a plan"""
    headline: str
    body: str

    def __str__(self):
        return f'''{self.headline}

{self.body}
        '''

    @classmethod
    def from_file(cls, path: Path):
        """Load a plan's message from a file"""
        try:
            with open(path, 'r') as file:
                plan_data = json.load(file)

            return PlanMessage(**plan_data['message'])
        except Exception as exc:
            raise GitPlanException(f'Failed to load plan from disk: {path}') from exc

    @classmethod
    def from_string(cls, string: str):
        """Construct a PlanMessage from a well-formatted string"""
        components = string.split('\n\n')
        if len(components) == 2:
            return PlanMessage(components[0], components[1])

        if len(components) > 2:
            return PlanMessage(components[0], '\n\n'.join(components[1:]))

        raise GitPlanException(f'Could not parse plan message from string: "{string}"')


@dataclass
class PlanId:
    """Represents the ID of a plan"""
    label: str
    number: int

    def __str__(self):
        return f"{self.label}-{self.number}"

    @classmethod
    def from_string(cls, value: str):
        parts = value.split('-')
        if len(parts) != 2:
            raise ValueError(f"Invalid PlanId: {value}")
        return PlanId(parts[0], int(parts[1]))


@dataclass
class Plan:
    """Represents a planned commit"""
    project: Project
    id: PlanId
    branch: str
    created_at: int
    updated_at: int
    _message: Optional[PlanMessage] = field(init=False, default=None)

    @property
    def filename(self):
        """The filename where this plan is stored

        Notes:
            TODO: How can we ensure backwards compatibility?
        """
        return f'commit-{self.id}'

    @property
    def path(self) -> Path:
        """The absolute path where this plan is stored"""
        return Path(self.project.plan_files_dir / self.filename).with_suffix(PLAN_FILE_EXT).resolve()

    @property
    def message(self):
        """Returns the plan message, loading it from disk if needed"""
        if not self._message:
            try:
                self.message = PlanMessage.from_file(self.path)
            except RuntimeError as exc:
                raise RuntimeError(f"Plan doesn't exist at location: {self.path}") from exc

        return self._message

    @message.setter
    def message(self, value: PlanMessage):
        self._message = value

    def save(self):
        """Persist the plan to the storage"""
        if not self._message:
            raise RuntimeError("Cannot save a plan with no message.")

        if not self.project.is_initialized:
            raise NotInitialized()

        if not self.created_at:
            raise ValueError("Missing created_at")

        if not self.created_at:
            raise ValueError("Missing updated_at")

        plan_dict = {
            "branch": self.branch.strip(),
            'message': {
                "headline": self.message.headline.strip(),
                "body": self.message.body.strip()
            },
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

        with open(self.path, 'w') as file:
            file.write(json.dumps(plan_dict))

    @classmethod
    def from_file(cls, file: Path, project: Project) -> "Plan":
        """Load a plan from a file"""
        with open(file, 'r') as fp:
            plan_data = json.load(fp)

        plan_message = PlanMessage(**plan_data['message'])
        plan_id_str = file.stem.split('-')[1]
        plan_id = PlanId.from_string(plan_id_str)
        branch = plan_data['branch']
        created_at = plan_data.get('created_at', time.time())
        updated_at = plan_data.get('updated_at', created_at)

        plan = Plan(
            project,
            plan_id,
            branch,
            int(created_at),
            int(updated_at)
        )
        plan.message = plan_message

        return plan

    def __str__(self):
        if not self._message:
            return super().__str__()
        return self._message.__str__()
