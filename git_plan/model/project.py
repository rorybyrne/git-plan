"""Project model

Author: Rory Byrne <rory@rory.bio>
"""

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from git_plan.constants import GP_DIR, GP_PROJECT_FNAME
from git_plan.exceptions import GitPlanException, NotInitialized
from git_plan.util import git
from git_plan.util.io import FlexibleEncoder


@dataclass
class Project:
    """A project"""

    root_dir: Path
    label: str = "FOO"

    @property
    def plan_dir(self) -> Path:
        """This project's .plan/ directory"""
        return Path(self.root_dir) / ".plan"

    @property
    def plan_files_dir(self) -> Path:
        """The directory where this project's plans are stored"""
        return self.plan_dir / "plans"

    @property
    def project_file(self) -> Path:
        """The file where project details are stored."""
        return self.plan_dir / GP_PROJECT_FNAME

    @property
    def is_initialized(self) -> bool:
        """Returns true if the project has a plan directory"""
        return (
            self.plan_dir.exists() and self.plan_files_dir.exists() and self.project_file.exists()
        )

    @property
    def is_a_git_repository(self) -> bool:
        """Returns whether or not the project is a git repository"""
        return git.is_git_repository(self.root_dir)

    @classmethod
    def from_dir(cls, root_dir: Path) -> "Project":
        """Returns a Project with the directory as its root"""
        gp_dir = root_dir / GP_DIR
        if not gp_dir.exists():
            raise NotInitialized()

        try:
            project_data = json.loads((gp_dir / GP_PROJECT_FNAME).read_text())
            return cls(**project_data)
        except Exception as e:
            raise NotInitialized() from e

    def save(self, to: Path):
        """Save the project info to the given file."""
        if not to.is_file() and to.suffix != ".json":
            raise GitPlanException(f"Invalid project filename: {to}")
        with open(to, encoding="utf8", mode="w") as fp:
            json.dump(asdict(self), fp, cls=FlexibleEncoder, indent=4)
