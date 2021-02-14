"""CLI entry point

Author: Rory Byrne <rory@rory.bio>
"""
import argparse
import os
import sys
from pathlib import Path

from dependency_injector.wiring import inject, Provide

from git_plan.cli.cli import CLI
from git_plan.containers import Application
from git_plan.exceptions import CommandNotFound


def parse_args():
    args_parser = argparse.ArgumentParser(prog='git-plan', description='A better workflow for git.')
    args_parser.add_argument('subcommand', type=str, nargs='?', help='The subcommand to run')
    return args_parser


@inject
def main(subcommand: str, cli: CLI = Provide[Application.cli]):
    """Entrypoint

    Parse CLI arguments and run the command.
    """
    try:
        command = cli.get_command(subcommand)
        command.run()
    except CommandNotFound:
        parser.print_help()
    except RuntimeError:
        raise


if __name__ == "__main__":
    working_dir = os.getcwd()
    parser = parse_args()
    args = parser.parse_args()

    app = Application()
    app.config.from_yaml('config.yaml')
    app.config.override({'plan_home': app.config.plan_home().replace('$HOME', str(Path.home()))})
    app.config.from_dict({
        'commands': {
            'working_dir': working_dir
        }
    })
    app.wire(modules=[sys.modules[__name__]])  # What is this? Who knows, but it works.

    main(args.subcommand)
