"""UI service

Author: Rory Byrne <rory@rory.bio>
"""
import datetime as dt
from typing import List

import humanize
import inquirer
from rich import print as rich_print

from git_plan.model.plan import Plan


class UIService:
    """Functionality for rendering in the terminal"""

    @staticmethod
    def choose_plan(plans: List[Plan], message: str):
        """Choose from a set of tasks"""
        if len(plans) == 0:
            raise RuntimeError("Cannot choose from an empty list of plans.")

        if len(plans) == 1:
            return plans[0]

        options = [
            inquirer.List(
                'plan',
                message=message,
                choices=[(c.message.headline, c) for c in plans]
            )
        ]

        answer = inquirer.prompt(options)

        return answer['plan']

    @staticmethod
    def confirm(message: str) -> bool:
        """Ask the user for confirmation"""
        key = 'confirm'
        questions = [inquirer.Confirm(key, message=message)]

        answers = inquirer.prompt(questions)

        return answers[key]

    def bold(self, message: str):
        """Print a bolded message"""
        self.print(f'[bold]{message}[/bold]')

    @staticmethod
    def print(message: str):
        """Print a message to the terminal"""
        rich_print(message)

    def render_plans(self, plans: List[Plan], headline_only=True):
        """Renders a list of plans in pretty print"""
        for idx, plan in enumerate(plans):
            self._render_plan(plan, str(idx + 1), headline_only)
            if idx < len(plans) - 1:
                print('')

    def _render_plan(self, plan: Plan, tag: str, headline_only):
        if not plan.updated_at:
            raise ValueError("Invalid plan: no updated_at field found.")

        time_display = f"[dim]({humanize.naturaltime(dt.datetime.fromtimestamp(plan.updated_at))})[/dim]"
        if headline_only:
            self.print(f'[bold][{tag}][/bold] {plan.message.headline} {time_display}')
        else:
            self.print(f'[bold][[magenta]{tag}[/magenta]][/bold] on {plan.branch} {time_display}\n')
            self.print(f'    {plan.message.headline}\n')
            body_lines = plan.message.body.split('\n')
            for line in body_lines:
                self.print(f'    {line}')
