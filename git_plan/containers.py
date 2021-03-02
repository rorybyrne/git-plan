"""Defines the dependency injection structure

@author Rory Byrne <rory@rory.bio>
"""

from dependency_injector import providers, containers

from git_plan.cli.cli import CLI
from git_plan.cli.commands.add import Add
from git_plan.cli.commands.edit import Edit
from git_plan.cli.commands.plan import Plan
from git_plan.oracle.oracle import Oracle
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
        task_template_file=config.app.task_template_file,
    )
    project_service = providers.Singleton(
        ProjectService,
        plan_home=config.app.plan_home,
        projects_file=config.app.projects_file
    )
    ui_service = providers.Singleton(
        UIService
    )


class Commands(containers.DeclarativeContainer):
    """Dependency structure for Commands"""
    config = providers.Configuration()
    services = providers.DependenciesContainer()

    plan_command = providers.Singleton(Plan, plan_service=services.plan_service, working_dir=config.project.working_dir)
    add_command = providers.Singleton(Add, plan_service=services.plan_service, working_dir=config.project.working_dir)
    edit_command = providers.Singleton(
        Edit,
        ui_service=services.ui_service,
        plan_service=services.plan_service,
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
            commands.add_command,
            commands.edit_command
        )
    )

    oracle = providers.Singleton(
        Oracle,
        plan_service=services.plan_service,
        plan_home=config.app.plan_home
    )
