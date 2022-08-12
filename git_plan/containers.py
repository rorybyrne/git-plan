"""Defines the dependency injection structure

@author Rory Byrne <rory@rory.bio>
"""
# pylint: disable=no-member
from dependency_injector import containers, providers

from git_plan.cli.cli import CLI
from git_plan.cli.commands.add import Add
from git_plan.cli.commands.commit import Commit
from git_plan.cli.commands.delete import Delete
from git_plan.cli.commands.edit import Edit
from git_plan.cli.commands.init import Init
from git_plan.cli.commands.list import List
from git_plan.cli.commands.migrate import Migrate
from git_plan.model.project import Project
from git_plan.service.git import GitService
from git_plan.service.migration import MigrationService
from git_plan.service.plan import PlanService
from git_plan.service.project import ProjectService
from git_plan.service.provider import ProviderService
from git_plan.service.ui import UIService


class Core(containers.DeclarativeContainer):
    """Global configuration for the system"""
    config = providers.Configuration()
    project = providers.Singleton(
        Project.from_dir,
        directory=config.working_dir
    )


class Services(containers.DeclarativeContainer):
    """Dependency structure for services"""
    config = providers.Configuration()
    core = providers.DependenciesContainer()

    git = providers.Singleton(GitService)
    provider = providers.Singleton(
        ProviderService,
        project_label=config.label
    )
    plan = providers.Singleton(
        PlanService,
        templates=providers.Dict(
            plan=config.template.plan,
            edit=config.template.edit
        ),
        git_service=git,
        provider_service=provider,
        project=core.project
    )
    migration = providers.Singleton(
        MigrationService,
        plan_service=plan,
        project=core.project
    )
    project = providers.Singleton(ProjectService)
    ui = providers.Singleton(UIService)


class Commands(containers.DeclarativeContainer):
    """Dependency structure for Commands"""
    config = providers.Configuration()
    services = providers.DependenciesContainer()
    core = providers.DependenciesContainer()

    list_command = providers.Singleton(
        List,
        plan_service=services.plan,
        ui_service=services.ui,
        git_service=services.git,
        project=core.project
    )
    add_command = providers.Singleton(
        Add,
        plan_service=services.plan,
        ui_service=services.ui,
        project=core.project
    )
    edit_command = providers.Singleton(
        Edit,
        ui_service=services.ui,
        plan_service=services.plan,
        project=core.project
    )
    delete_command = providers.Singleton(
        Delete,
        ui_service=services.ui,
        plan_service=services.plan,
        project=core.project
    )
    commit_command = providers.Singleton(
        Commit,
        ui_service=services.ui,
        plan_service=services.plan,
        git_service=services.git,
        project=core.project
    )
    init_command = providers.Singleton(
        Init,
        project_service=services.project,
        ui_service=services.ui,
        project=core.project
    )
    migrate_command = providers.Singleton(
        Migrate,
        project=core.project,
        ui_service=services.ui,
        migration_service=services.migration
    )


class Application(containers.DeclarativeContainer):
    """Top-level container for the application"""
    config = providers.Configuration()

    core = providers.Container(
        Core,
        config=config
    )

    services = providers.Container(
        Services,
        config=config,
        core=core
    )

    commands = providers.Container(
        Commands,
        config=config,
        services=services,
        core=core
    )

    # Entrypoints
    cli = providers.Singleton(
        CLI,
        commands=providers.List(
            commands.list_command,
            commands.add_command,
            commands.edit_command,
            commands.commit_command,
            commands.init_command,
            commands.delete_command,
            commands.migrate_command
        ),
        plan_service=services.plan,
        migration_service=services.migration,
        ui_service=services.ui,
    )
