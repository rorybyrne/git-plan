"""Local Provider"""

from git_plan.service.providers.provider import Provider


class LocalProvider(Provider):
    """Provider for local plans - i.e. not involving a third-party service like Linear"""
