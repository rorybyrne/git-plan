"""List command

@author Rory Byrne <rory@rory.bio>
"""
from argparse import ArgumentParser
from typing import Any

from git_plan.cli.commands.command import Command
from git_plan.exceptions import NotAGitRepository
from git_plan.service.git import GitService
from git_plan.service.plan import PlanService
from git_plan.util.decorators import requires_initialized, requires_git_repository


@requires_initialized
@requires_git_repository
class List(Command):
    """List commits."""

    subcommand = 'list'

    def __init__(self, plan_service: PlanService, git_service: GitService, **kwargs):
        super().__init__(**kwargs)
        assert plan_service, "Plan service not injected"
        self._plan_service = plan_service
        self._git = git_service

    def command(self, *, long: bool = False, branch: bool = None, **kwargs):  # pylint: disable=arguments-differ
        """List the planned commits"""
        if not self._repository:
            raise NotAGitRepository()

        if branch:
            filter_branch = self._git.get_current_branch()
        else:
            filter_branch = None

        branch_display = filter_branch if filter_branch else "all branches"
        self._ui.print(f"Plans for [bold]{branch_display}[/bold]\n")
        commits = self._plan_service.get_commits(self._repository, branch=branch)

        if len(commits) == 0:
            if branch:
                self._ui.bold("No commit plans on the current branch.")
            else:
                self._ui.bold("No commit plans.")

            return

        commits = sorted(commits, key=lambda c: c.id)
        self._ui.render_commits(commits, headline_only=not long)

    def register_subparser(self, subparsers: Any):
        parser: ArgumentParser = subparsers.add_parser(List.subcommand, help='List existing commit plans.')
        parser.add_argument('-l', '--long', dest='long', action='store_true')
        parser.add_argument(
            '-b',
            '--branch',
            dest='branch',
            action='store_true',
            help='Show plans for the current branch'
        )
