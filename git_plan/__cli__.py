"""CLI entry point

Author: Rory Byrne <rory@rory.bio>
"""
import os
import sys
from pathlib import Path
from typing import List

from dependency_injector.wiring import inject, Provide

from git_plan.cli.cli import CLI
from git_plan.containers import Application

HOME = str(Path.home())
CONFIG_DIR = os.path.join(HOME, '.local', 'share', 'git-plan')


@inject
def main(args: List[str], cli: CLI = Provide[Application.cli]):
    """Entrypoint"""
    cli.parse(args)


if __name__ == "__main__":
    working_dir = os.getcwd()
    args = sys.argv[1:]  # Might be []

    app = Application()
    config_file = os.path.join(CONFIG_DIR, 'config.yaml')
    if not os.path.exists(config_file):
        raise RuntimeError(f'Config file not found at: "{config_file}"')
    app.config.from_yaml(config_file)
    app.config.set('app.plan_home', app.config.app.plan_home().replace('$HOME', HOME))
    app.config.set('project.working_dir', working_dir)
    app.wire(modules=[sys.modules[__name__]])  # What is this? Who knows, but it works.

    main(args)
