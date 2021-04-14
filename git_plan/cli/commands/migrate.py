"""Migrate command

Migrate data from the old format to the new
"""
from typing import Any

from git_plan.cli.commands.command import Command
from git_plan.service.migration import MigrationService


class Migrate(Command):
    """Migrate old plans to the new format"""

    subcommand = "migrate"

    def __init__(self, migration_service: MigrationService, **kwargs):
        super().__init__(**kwargs)
        assert migration_service
        self._migration_service: MigrationService = migration_service

    def command(self, **kwargs):
        """Attempt to load old plans, and if any have the wrong format then offer to migrate"""
        if not self._migration_service.should_migrate():
            self._ui.bold("No migration needed.")
            return

        if not self._ui.confirm("This will update each of your plan files to the new format. Continue?"):
            self._ui.bold("Aborting migration.")
            return

        try:
            self._migration_service.backup()
            self._ui.bold("We backed up your .plan directory to .plan.bkp")
            self._migration_service.migrate()
            self._ui.bold("Migration complete. Please test that git-plan works, and then delete the backup directory.")
        except Exception as e:
            self._ui.bold(f"Migration failed: {str(e)}")
            raise


    def register_subparser(self, subparsers: Any):
        subparsers.add_parser(self.subcommand, help='Migrate plans to the new format.')
