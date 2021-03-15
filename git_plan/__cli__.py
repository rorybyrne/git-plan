"""CLI entry point

Author: Rory Byrne <rory@rory.bio>
"""
from git_plan.conf import Settings
import os
import sys
from pathlib import Path
from typing import List

from dependency_injector.wiring import inject, Provide

from git_plan.cli.cli import CLI
from git_plan.containers import Application
from git_plan.exceptions import ProjectNotInitialized

HOME = str(Path.home())
CONFIG_DIR = os.path.join(HOME, '.local', 'share', 'git-plan')


def main():
    """Entrypoint"""
    settings = Settings.load()

    app = Application()
    app.config.from_dict(settings)
    app.wire(modules=[sys.modules[__name__]])

    try:
        args = sys.argv[1:]  # Might be []
        launch_cli(args)
    except ProjectNotInitialized as e:
        print("Git plan is not initialized.\n\tPlease run `git plan init`")


@inject
def launch_cli(args: List[str], cli: CLI = Provide[Application.cli]):
    cli.parse(args)


if __name__ == "__main__":
    main()
