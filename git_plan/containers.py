"""Defines the dependency injection structure

@author Rory Byrne <rory@rory.bio>
"""
from pathlib import Path

from dependency_injector import providers, containers

from git_plan.cli.cli import CLI
from git_plan.cli.commands.add import Add
from git_plan.cli.commands.plan import Plan
from git_plan.oracle.oracle import Oracle
from git_plan.service.observer import ObserverService
from git_plan.service.plan import PlanService


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
        projects_file=config.app.projects_file
    )
    observer_service = providers.Singleton(ObserverService)


class Commands(containers.DeclarativeContainer):
    """Dependency structure for Commands"""
    config = providers.Configuration()
    services = providers.DependenciesContainer()

    plan_command = providers.Singleton(Plan, plan_service=services.plan_service, working_dir=config.project.working_dir)
    add_command = providers.Singleton(Add, plan_service=services.plan_service, working_dir=config.project.working_dir)


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
            commands.add_command
        )
    )

    oracle = providers.Singleton(
        Oracle,
        plan_service=services.plan_service,
        plan_home=config.app.plan_home
    )
