"""Configuration

Author: Rory Byrne <rory@rory.bio>
"""
from pathlib import Path

from git_plan import constants


class Settings(dict):
    """Responsible for loading all settings from disk/defaults before starting the app

    Here, user-defined settings like custom templates can be loaded.
    """

    # Builders ####################################################################################

    @staticmethod
    def _from_project() -> dict:
        """Attempt to load a config.yaml from the local git repository"""
        return {}

    @staticmethod
    def _from_local() -> dict:
        """Attempt to load a config.yaml from a default directory"""
        return {}

    @staticmethod
    def _default() -> dict:
        """Return the default settings"""
        return constants.DEFAULT_SETTINGS

    @staticmethod
    def load() -> "Settings":
        """Load the settings"""
        settings = Settings._default()
        local_settings = Settings._from_local()
        project_settings = Settings._from_project()

        local_settings.update(project_settings)  # Roll project into local settings
        settings.update(local_settings)  # Roll both into the default settings

        cwd = Path.cwd()
        settings["working_dir"] = cwd

        return Settings(settings)
