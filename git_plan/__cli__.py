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
from git_plan.exceptions import ProjectNotInitialized

HOME = str(Path.home())
CONFIG_DIR = os.path.join(HOME, '.local', 'share', 'git-plan')


def main():
    """Entrypoint"""
    app = Application()
    configure(app)
    app.wire(modules=[sys.modules[__name__]])  # What is this? Who knows, but it works.

    try:
        args = sys.argv[1:]  # Might be []
        launch_cli(args)
    except ProjectNotInitialized as e:
        print("Git plan is not initialized.\n\tPlease run `git plan init`")


@inject
def launch_cli(args: List[str], cli: CLI = Provide[Application.cli]):
    cli.parse(args)


def configure(app: Application):
    working_dir = os.getcwd()
    config_file = os.path.join(CONFIG_DIR, 'config.yaml')
    if not os.path.exists(config_file):
        raise RuntimeError(f'Config file not found at: "{config_file}"')

    app.config.from_yaml(config_file)
    plan_home = app.config.app.plan_home().replace('$HOME', HOME)
    app.config.set('app.plan_home', plan_home)
    app.config.set('project.working_dir', working_dir)
    app.config.set('app.edit_template_file', os.path.join(plan_home, app.config.app.edit_template_file()))
    app.config.set('app.commit_template_file', os.path.join(plan_home, app.config.app.commit_template_file()))
    app.config.set('app.projects_file', os.path.join(plan_home, app.config.app.projects_file()))


if __name__ == "__main__":
    main()
