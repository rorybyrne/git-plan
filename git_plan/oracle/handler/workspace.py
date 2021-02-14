"""Workspace event handler

Author: Rory Byrne <rory@rory.bio>
"""
from watchdog.events import FileSystemEventHandler, FileSystemEvent


class WorkspaceEventHandler(FileSystemEventHandler):

    def on_modified(self, event: FileSystemEvent):
        """Handle modification events

        0. Ignore if it's in .gitignore
        1. Check if it's a file modification
        2. Check if the file name is mentioned in the plan
        3. If not, fire an event

        @param event: The event
        """
        print(f"Modified:\t {event.src_path}")
