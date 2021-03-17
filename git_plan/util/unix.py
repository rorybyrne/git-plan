"""Unix utilities

Author Rory Byrne <rory@rory.bio>
"""
from shutil import which


def is_installed(name: str) -> bool:
    """Check whether `name` is on PATH and marked as executable."""
    return which(name) is not None
