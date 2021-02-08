"""Observer service

@author Rory Byrne <rory@rory.bio>
"""


class ObserverService:

    def create_observer(self, directory: str):
        """Create an observer in the given directory

        1. Launch a background thread
        2. Store the PID in a file in .git/
        """
        pass

    def kill_all(self):
        """Kill all active observers for the current repository

        1. Find PID(s) from file in .git/
        2. Kill processes
        """
        pass

    def kill_one(self, pid: str):
        """Kill the process with a given PID"""
        pass
