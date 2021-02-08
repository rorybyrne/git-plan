"""Defines the dependency injection structure

@author Rory Byrne <rory@rory.bio>
"""
from dependency_injector import providers, containers

from git_plan.cli import CLI
from git_plan.commands.kill import Kill
from git_plan.commands.plan import Plan
from git_plan.service.observer import ObserverService
from git_plan.service.plan import PlanService


class Core(containers.DeclarativeContainer):
    """Global configuration for the system"""
    config = providers.Configuration()


class Services(containers.DeclarativeContainer):
    """Dependency structure for services"""
    config = providers.Configuration()

    plan_service = providers.Singleton(PlanService, directory=config.directory)
    observer_service = providers.Singleton(ObserverService)


class Commands(containers.DeclarativeContainer):
    """Dependency structure for Commands"""
    config = providers.Configuration()
    services = providers.DependenciesContainer()

    plan_command = providers.Singleton(Plan, plan_service=services.plan_service)
    kill_command = providers.Singleton(Kill, observer_service=services.observer_service)


class Application(containers.DeclarativeContainer):
    """Top-level container for the application"""
    config = providers.Configuration()

    core = providers.Container(
        Core,
        config=config.core
    )

    services = providers.Container(
        Services,
        config=config.services
    )

    commands = providers.Container(
        Commands,
        config=config.commands,
        services=services
    )

    cli = providers.Singleton(
        CLI,
        commands=providers.List(
            commands.plan_command, commands.kill_command
        )
    )
