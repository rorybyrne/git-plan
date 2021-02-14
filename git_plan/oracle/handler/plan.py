"""Plan event handler

Author: Rory Byrne <rory@rory.bio>
"""
from time import time
from typing import TYPE_CHECKING, Tuple

from cachetools import LRUCache

if TYPE_CHECKING:  # Always False at runtime, to avoid cyclic dependencies
    from git_plan.oracle.oracle import Oracle

from watchdog.events import FileSystemEventHandler, FileSystemEvent

from git_plan.service.plan import PlanService

TimedEvent = Tuple[int, str]


class PlanEventHandler(FileSystemEventHandler):
    """Handle changes to the plan directory"""

    def __init__(self, oracle: "Oracle", plan_service: PlanService):
        self._oracle = oracle
        self._plan_service = plan_service

        self._cache = LRUCache(256)

    def on_created(self, event: FileSystemEvent):
        """Pass the event to the Guru to update the plan state"""
        if self._should_handle(event):
            print('\tPLAN CREATED')
            print(event)
            plan_dirs = self._plan_service.load_plans()
            self._oracle.reconcile(plan_dirs)

    def on_modified(self, event: FileSystemEvent):
        """Handles the modification event"""
        if self._should_handle(event):
            plan_dirs = self._plan_service.load_plans()
            self._oracle.reconcile(plan_dirs)

    def _should_handle(self, event: FileSystemEvent):
        """Determine whether or not we should handle this event, or skip it

        Notes:
            There might be a race condition when the `seconds` value is at x.99999
        """
        seconds = int(time())
        if not event.is_directory and event.src_path.endswith('plans.json'):
            return False

        timed_event = (seconds, event.src_path)
        is_duplicate = timed_event in self._cache
        if is_duplicate:
            self._cache[timed_event] = event
            return False

        return True
