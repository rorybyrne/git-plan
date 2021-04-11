"""Provider Service

Functionality relating to Plan Providers
"""

from git_plan.service.providers.local import LocalProvider
from git_plan.service.providers.provider import Provider


class ProviderException(Exception):
    """An exception happened in the provider service"""


class ProviderService:
    LOCAL = "local"

    def __init__(self, project_label: str):
        self._project_label = project_label

    def get_by_name(self, name: str) -> Provider:
        """Tries to get the Provider by its name, and raises a ProviderException if it cannot be found"""
        if name == self.LOCAL:
            return LocalProvider(self._project_label)
        else:
            raise ProviderException(f"Provider not found: {name}")

    def get_local_provider(self) -> LocalProvider:
        """Get an instance of LocalProvider"""
        return LocalProvider(self._project_label)
