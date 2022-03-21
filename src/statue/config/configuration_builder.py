"""Singleton class for building configuration instances."""
import sys
from pathlib import Path
from typing import Any, MutableMapping, Optional, Union

import toml

from statue.config.configuration import Configuration
from statue.constants import COMMANDS, CONTEXTS, GENERAL, MODE, SOURCES
from statue.exceptions import InvalidConfiguration, MissingConfiguration
from statue.runner import RunnerMode

if sys.version_info < (3, 9):  # pragma: no cover
    from importlib_resources.abc import Traversable
else:  # pragma: no cover
    from importlib.abc import Traversable


class ConfigurationBuilder:
    """Build configuration instances from configuration file."""

    @classmethod
    def build_configuration_from_file(
        cls,
        statue_configuration_path: Optional[Union[Path, Traversable]] = None,
        cache_dir: Optional[Path] = None,
    ) -> Configuration:
        """
        Load statue configuration.

        This method combines default configuration with user-defined configuration, read
        from configuration file.

        :param statue_configuration_path: User-defined file path containing
            repository-specific configurations
        :type statue_configuration_path: Optional[Path]
        :param cache_dir: Optional Caching directory
        :type cache_dir: Optional[Path]
        :return: Configuration instance
        :rtype: Configuration
        :raises MissingConfiguration: Raised when could not load
        """
        if statue_configuration_path is None:
            statue_configuration_path = cls.configuration_path()
        if (
            isinstance(statue_configuration_path, Path)
            and not statue_configuration_path.exists()
        ):
            raise MissingConfiguration()
        with statue_configuration_path.open(mode="r") as configuration_file:
            statue_config = toml.load(configuration_file)
        cache_dir = cls.cache_path(Path.cwd()) if cache_dir is None else cache_dir
        configuration = Configuration(cache_root_directory=cache_dir)
        cls.update_from_config(configuration=configuration, statue_config=statue_config)
        return configuration

    @classmethod
    def update_from_config(
        cls, configuration: Configuration, statue_config: MutableMapping[str, Any]
    ):
        """
        Update configuration from a loaded config map.

        :param configuration: Configuration instance to be updated
        :type configuration: Configuration
        :param statue_config: Configuration map as loaded from config file
        :type statue_config: MutableMapping[str, Any]
        :raises InvalidConfiguration: Raised when some fields are invalid
            in configuration
        """
        general_configuration = statue_config.get(GENERAL, {})
        if MODE in general_configuration:
            mode = general_configuration[MODE].upper()
            try:
                configuration.default_mode = RunnerMode[mode]
            except KeyError as error:
                raise InvalidConfiguration(
                    f"Got unexpected runner mode in configuration: {mode}"
                ) from error
        if CONTEXTS in statue_config:
            configuration.contexts_repository.update_from_config(
                statue_config[CONTEXTS]
            )
        if SOURCES in statue_config:
            configuration.sources_repository.update_from_config(
                config=statue_config[SOURCES],
                contexts_repository=configuration.contexts_repository,
            )
        if COMMANDS in statue_config:
            configuration.commands_repository.update_from_config(
                statue_config[COMMANDS]
            )

    @classmethod
    def configuration_path(cls, directory: Optional[Path] = None) -> Path:
        """
        Search for configuration file in directory.

        :param directory: Directory in which the configuration path is supposed to be
        :type directory: Path
        :return: Configuration path location
        :rtype: Path
        """
        if directory is None:
            directory = Path.cwd()
        return directory / "statue.toml"

    @classmethod
    def cache_path(cls, directory: Path) -> Path:
        """
        Default caching directory for statue history saving.

        :param directory: Directory in which cache directory will be created
        :type directory: Path
        :return: Cache directory
        :rtype: Path
        """
        return directory / ".statue"
