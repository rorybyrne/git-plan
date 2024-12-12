"""Unix utilities

Author Rory Byrne <rory@rory.bio>
"""

from shutil import which
import subprocess
from typing import Optional, Sequence


def is_installed(name: str) -> bool:
    """Check whether `name` is on PATH and marked as executable."""
    return which(name) is not None


def run_command(cmd: Sequence[str], capture_output: bool = True) -> Optional[str]:
    """Run a shell command"""
    result = subprocess.run(cmd, capture_output=capture_output, check=True)
    if result.stdout:
        return result.stdout.decode()

    return None
