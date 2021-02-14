"""Entry point for the Oracle

Author: Rory Byrne <rory@rory.bio>
"""
import sys
from pathlib import Path

from dependency_injector.wiring import inject, Provide

from git_plan.containers import Application
from git_plan.oracle.oracle import Oracle


@inject
def main(oracle: Oracle = Provide[Application.oracle]):
    oracle.start()


if __name__ == "__main__":
    app = Application()
    app.config.from_yaml('config.yaml')
    app.config.override({'plan_home': app.config.plan_home().replace('$HOME', str(Path.home()))})
    app.wire(modules=[sys.modules[__name__]])  # What is this? Who knows, but it works.

    main()
