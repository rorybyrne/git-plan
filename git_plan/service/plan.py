"""Plan service

@author Rory Byrne <rory@rory.bio>
"""
import json
import os
import tempfile
from subprocess import call


class PlanService:

    def create_plan(self) -> str:
        """Create a plan in the given directory

        1. Create a new file in .git/ containing the plan
        """
        plan = self._ask_for_plan()

        return plan

    def save_plan(self, plan: str, directory: str):
        self._write_plan(plan, directory)

    def update_plan(self, new_plan: str, directory: str):
        """Update the plan in the given directory"""
        pass

    def delete_plan(self, directory: str):
        pass

    def plan_exists(self, directory: str):
        """Check if a plan already exists in the given directory"""
        return os.path.isfile(self._plan_filename(directory))

    def print_status(self, directory: str):
        """Print the status of the plan"""
        plan = self._read_plan(directory)
        if not plan:
            raise RuntimeError("Plan not found?")

        print("Plan:")
        print(plan)

    @staticmethod
    def load_plans(plan_home: str):
        """Returns a list of directories"""
        try:
            plans_file = os.path.join(plan_home, 'plans.json')
            with open(plans_file) as ph:
                plan_data = json.load(ph)

            return plan_data['plans']
        except FileNotFoundError:
            print("Couldn't find plans file")
            return []


    # Private #############

    @staticmethod
    def local_plan_dir(directory: str):
        return f'{directory}/.git/plan'

    def _plan_filename(self, directory: str):
        return f'{self.local_plan_dir(directory)}/plan.txt'

    def _read_plan(self, directory: str):
        plan_filename = f'{directory}/.git/plan/plan.txt'
        with open(plan_filename, 'r') as f:
            return f.read()

    def _write_plan(self, plan: str, directory: str):
        """Writes/overwrites the plan file"""
        if not self._is_git_repository(directory):
            raise RuntimeError("Not a git repository")

        os.makedirs(os.path.dirname(self._plan_filename(directory)), exist_ok=True)  # Create plan/ directory if needed

        with open(self._plan_filename(directory), 'w') as f:
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
