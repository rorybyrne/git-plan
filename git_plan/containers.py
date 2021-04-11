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
from git_plan.model.repository import Repository
from git_plan.service.git import GitService
from git_plan.service.plan import PlanService
from git_plan.service.repository import RepositoryService
from git_plan.service.ui import UIService


class Core(containers.DeclarativeContainer):
    """Global configuration for the system"""
    config = providers.Configuration()
    repository = providers.Singleton(
        Repository.from_working_dir,
        working_dir=config.working_dir
    )


class Services(containers.DeclarativeContainer):
    """Dependency structure for services"""
    config = providers.Configuration()

    git_service = providers.Singleton(GitService)
    plan_service = providers.Singleton(
        PlanService,
        plan_template=config.template.plan,
        edit_template=config.template.edit,
        git_service=git_service,
    )
    repository = providers.Singleton(RepositoryService)
    ui_service = providers.Singleton(UIService)


class Commands(containers.DeclarativeContainer):
    """Dependency structure for Commands"""
    config = providers.Configuration()
    services = providers.DependenciesContainer()
    core = providers.DependenciesContainer()

    list_command = providers.Singleton(
        List,
        plan_service=services.plan_service,
        ui_service=services.ui_service,
        git_service=services.git_service,
        repository=core.repository
    )
    add_command = providers.Singleton(
        Add,
        plan_service=services.plan_service,
        ui_service=services.ui_service,
        repository=core.repository
    )
    edit_command = providers.Singleton(
        Edit,
        ui_service=services.ui_service,
        plan_service=services.plan_service,
        repository=core.repository
    )
    delete_command = providers.Singleton(
        Delete,
        ui_service=services.ui_service,
        plan_service=services.plan_service,
        repository=core.repository
    )
    commit_command = providers.Singleton(
        Commit,
        ui_service=services.ui_service,
        plan_service=services.plan_service,
        git_service=services.git_service,
        repository=core.repository
    )
    init_command = providers.Singleton(
        Init,
        repository_service=services.repository,
        ui_service=services.ui_service,
        repository=core.repository
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
            commands.delete_command
        ),
        plan_service = services.plan_service,
        repository = core.repository
    )
