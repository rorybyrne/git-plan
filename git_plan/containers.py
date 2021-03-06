"""Defines the dependency injection structure

@author Rory Byrne <rory@rory.bio>
"""
from dependency_injector import providers, containers

from git_plan.cli.cli import CLI
from git_plan.cli.commands.add import Add
from git_plan.cli.commands.commit import Commit
from git_plan.cli.commands.edit import Edit
from git_plan.cli.commands.list import List
from git_plan.cli.commands.plan import Plan
from git_plan.service.git import GitService
from git_plan.service.plan import PlanService
from git_plan.service.project import ProjectService
from git_plan.service.ui import UIService


class Core(containers.DeclarativeContainer):
    """Global configuration for the system"""
    config = providers.Configuration()


class Services(containers.DeclarativeContainer):
    """Dependency structure for services"""
    config = providers.Configuration()

    plan_service = providers.Singleton(
        PlanService,
        plan_home=config.app.plan_home,
        commit_template_file=config.app.commit_template_file,
    )
    project_service = providers.Singleton(
        ProjectService,
        plan_home=config.app.plan_home,
        projects_file=config.app.projects_file
    )
    ui_service = providers.Singleton(
        UIService
    )
    git_service = providers.Singleton(
        GitService
    )


class Commands(containers.DeclarativeContainer):
    """Dependency structure for Commands"""
    config = providers.Configuration()
    services = providers.DependenciesContainer()

    plan_command = providers.Singleton(
        Plan,
        plan_service=services.plan_service,
        working_dir=config.project.working_dir
    )
    list_command = providers.Singleton(
        List,
        plan_service=services.plan_service,
        ui_service=services.ui_service,
        working_dir=config.project.working_dir
    )
    add_command = providers.Singleton(
        Add,
        plan_service=services.plan_service,
        working_dir=config.project.working_dir
    )
    edit_command = providers.Singleton(
        Edit,
        ui_service=services.ui_service,
        plan_service=services.plan_service,
        working_dir=config.project.working_dir
    )
    commit_command = providers.Singleton(
        Commit,
        ui_service=services.ui_service,
        plan_service=services.plan_service,
        git_service=services.git_service,
        working_dir=config.project.working_dir
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
        config=config
    )

    commands = providers.Container(
        Commands,
        config=config,
        services=services
    )

    # Entrypoints
    cli = providers.Singleton(
        CLI,
        commands=providers.List(
            commands.plan_command,
            commands.list_command,
            commands.add_command,
            commands.edit_command,
            commands.commit_command
        )
    )
