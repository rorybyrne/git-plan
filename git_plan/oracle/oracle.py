"""Oracle

@author Rory Byrne <rory@rory.bio>
"""
from time import sleep
from typing import Dict

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from watchdog.observers.api import ObservedWatch

from git_plan.oracle.handler.plan import PlanEventHandler
from git_plan.oracle.handler.workspace import WorkspaceEventHandler
from git_plan.service.plan import PlanService


class Oracle:
    """Observe the active workspaces"""

    def __init__(self, plan_service: PlanService, plan_home: str):
        self._observer = Observer()
        self._plan_service = plan_service
        self._plan_home = plan_home

        self._watches_by_dir: Dict[str, ObservedWatch] = dict()

        # Handlers
        self._plan_handler = PlanEventHandler(self, self._plan_service)
        self._workspace_handler = WorkspaceEventHandler()

    def start(self):
        """Observe the plan directory and any subsequently registered directories"""
        assert self._plan_service, "Plan service missing"
        assert self._plan_home, "Path is missing"

        # Watch the plan_home directory
        self.watch(self._plan_home, self._plan_handler, recursive=False)
        self._observer.start()

        # Watch the registered workspaces
        workspaces = self._plan_service.load_plans()
        workspace_handler = WorkspaceEventHandler()
        if len(workspaces) == 0:
            print("No plans!")
        else:
            for workspace in workspaces:
                self.watch(workspace, workspace_handler)

        try:
            while True:
                sleep(1)
        except KeyboardInterrupt:
            self._observer.stop()
        self._observer.join()

    def watch(self, directory: str, handler: FileSystemEventHandler, recursive=False):
        watch = self._observer.schedule(handler, directory, recursive=recursive)
        self._watches_by_dir[directory] = watch

        print(f'Watched {directory}')

    def reconcile(self, workspaces: str):
        """Watch any new workspaces, and un-watch any which have been removed"""
        watched_workspaces = [d for d in self._watched_paths if d != self._plan_home]
        for ws in workspaces:
            if ws not in watched_workspaces:
                self.watch(ws, WorkspaceEventHandler())

        for watched_workspace in watched_workspaces:
            if watched_workspace not in workspaces:
                to_remove = watched_workspace
                print(f'Unwatching {to_remove}')
                self.unwatch(to_remove)

    def unwatch(self, workspace: str):
        watch = self._watches_by_dir[workspace]
        self._observer.unschedule(watch)
        del self._watches_by_dir[workspace]

    @property
    def _watched_paths(self):
        return self._watches_by_dir.keys()
