"""Unix utilities

Author Rory Byrne <rory@rory.bio>
"""
import subprocess
from shutil import which
from typing import List, Optional


def is_installed(name: str) -> bool:
    """Check whether `name` is on PATH and marked as executable."""
    return which(name) is not None


def run_command(cmd: List[str], capture_output: bool = True) -> Optional[str]:
    """Run a shell command"""
    result = subprocess.run(cmd, capture_output=capture_output, check=True)
    if result.stdout:
        return result.stdout.decode()

    return None


def shell_is_in_git_repository():
    """Uses the git tool in a shell to check whether the current directory is in a repository"""
    command = 'git rev-parse --is-inside-work-tree'
    cmd = command.split(' ')
    try:
        run_command(cmd)
        return True
    except subprocess.CalledProcessError:
        return False
