import argparse
import os
import sys

from dependency_injector.wiring import inject, Provide

from git_plan.cli import CLI
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
    parser = parse_args()
    args = parser.parse_args()

    app = Application()
    cwd = os.getcwd()
    app.config.from_dict({
        'services': {
            'directory': cwd
        }
    })
    app.wire(modules=[sys.modules[__name__]])  # What is this? Who knows, but it works.

    main(args.subcommand)
