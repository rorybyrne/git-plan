"""Plan service

@author Rory Byrne <rory@rory.bio>
"""
import os
import tempfile
from subprocess import call


class PlanService:

    def __init__(self, directory: str):
        assert directory, "Directory is None"
        self._directory = directory

    def create_plan(self):
        """Create a plan in the given directory

        1. Create a new file in .git/ containing the plan
        """
        plan = self._ask_for_plan()
        self._write_plan(plan, self._directory)

    def update_plan(self, new_plan: str, directory: str):
        """Update the plan in the given directory"""
        pass

    def plan_exists(self):
        """Check if a plan already exists in the given directory"""
        return os.path.isfile(self._plan_filename)

    def print_status(self):
        """Print the status of the plan"""
        plan = self._read_plan()
        if not plan:
            raise RuntimeError("Plan not found?")

        print("Plan:")
        print(plan)

    # Private #############

    @property
    def _plan_home(self):
        return f'{self._directory}/.git/plan'

    @property
    def _plan_filename(self):
        return f'{self._plan_home}/plan.txt'

    def _read_plan(self):
        plan_filename = f'{self._directory}/.git/plan/plan.txt'
        with open(plan_filename, 'r') as f:
            return f.read()

    def _write_plan(self, plan: str, directory: str):
        """Writes/overwrites the plan file"""
        if not self._is_git_repository(directory):
            raise RuntimeError("Not a git repository")

        os.makedirs(os.path.dirname(self._plan_filename), exist_ok=True)  # Create plan/ directory if needed

        with open(self._plan_filename, 'w') as f:
            f.write(plan)

    @staticmethod
    def _ask_for_plan():
        editor = os.environ.get('EDITOR', 'vim')
        initial_message = ''

        with tempfile.NamedTemporaryFile(suffix=".tmp", mode='r+') as tf:
            tf.write(initial_message)
            tf.flush()
            call([editor, tf.name])

            tf.seek(0)
            edited_message = tf.read()

            return edited_message

    @staticmethod
    def _is_git_repository(directory: str):
        """Checks whether a .git/ directory exists

        @todo   move this to utilities so it can be re-used elsewhere
        """
        return os.path.isdir(f'{directory}/.git')
