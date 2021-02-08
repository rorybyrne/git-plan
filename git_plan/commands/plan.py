"""Plan command

@author Rory Byrne <rory@rory.bio>
"""
from git_plan.commands.command import Command


class Plan(Command):
    """Create or update a plan."""

    def pre_command(self):
        """Check whether a plan already exists?"""
        pass

    def command(self):
        """Use the PlanService to create the plan in the local .git/ directory

        1. Present a VIM editor with the PLAN_MSG template
        2. Save the result to a stable location (@todo)
        3. Launch an observer to watch the development environment
            3a. When does the observer terminate?
        """
        pass
