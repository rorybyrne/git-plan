import argparse

from git_plan.commands.kill import Kill
from git_plan.commands.plan import Plan


def parse_args():
    args_parser = argparse.ArgumentParser(prog='git-plan', description='A better workflow for git.')
    args_parser.add_argument('subcommand', type=str, nargs='?', help='The subcommand to run')
    return args_parser


if __name__ == "__main__":
    parser = parse_args()
    args = parser.parse_args()
    if not args.subcommand:
        Plan.run()
    elif args.subcommand == 'kill':
        Kill.run()
    else:
        parser.print_help()
