"""CLI entry point

Author: Rory Byrne <rory@rory.bio>
"""
import sys
from pathlib import Path
from typing import List

from dependency_injector.wiring import inject, Provide

from git_plan.cli.cli import CLI
from git_plan.conf import Settings
from git_plan.containers import Application
from git_plan.exceptions import NotAGitRepository, NotInitialized, GitPlanException

HOME = str(Path.home())


def main():
    """Entrypoint"""
    settings = Settings.load()

    app = Application()
    app.config.from_dict(settings)
    app.wire(modules=[sys.modules[__name__]])

    args = sys.argv[1:]  # Might be []

    try:
        launch_cli(args)
    except NotInitialized:
        print("Git plan is not initialized.\n\tPlease run `git plan init`")
    except NotAGitRepository:
        print("You are not in a git repository (no .git/ directory found).")
    except GitPlanException as exc:
        print("git plan encountered an error.")
        print("Please open an issue at https://github.com/synek/git-plan and let us know.\n")
        print(f"The error message was '{str(exc)}'")


@inject
def launch_cli(args: List[str], cli: CLI = Provide[Application.cli]):
    """Inject dependency tree and run the CLI"""
    cli.parse(args)


if __name__ == "__main__":
    main()
