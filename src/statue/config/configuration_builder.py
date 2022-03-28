"""Singleton class for building configuration instances."""
import sys
from pathlib import Path
from typing import Any, MutableMapping, Optional, Union

import tomli

from statue.cache import Cache
from statue.config.configuration import Configuration
from statue.constants import (
    COMMANDS,
    CONTEXTS,
    DEFAULT_HISTORY_SIZE,
    GENERAL,
    HISTORY_SIZE,
    MODE,
    SOURCES,
)
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
        with statue_configuration_path.open(mode="rb") as configuration_file:
            statue_config = tomli.load(configuration_file)
        cache_dir = cls.cache_path(Path.cwd()) if cache_dir is None else cache_dir
        return cls.from_dict(cache_dir=cache_dir, statue_config_dict=statue_config)

    @classmethod
    def from_dict(
        cls, cache_dir: Path, statue_config_dict: MutableMapping[str, Any]
    ) -> Configuration:
        """
        Build configuration from a loaded config map.

        :param cache_dir: Directory for keeping cache.
        :type cache_dir: Path
        :param statue_config_dict: Configuration map as loaded from config file
        :type statue_config_dict: MutableMapping[str, Any]
        :return: Built configuration instance
        :type: Configuration
        :raises InvalidConfiguration: Raised when some fields are invalid
            in configuration
        """
        general_configuration = statue_config_dict.get(GENERAL, {})
        history_size = general_configuration.get(HISTORY_SIZE, DEFAULT_HISTORY_SIZE)
        cache = Cache(cache_root_directory=cache_dir, size=history_size)
        configuration = Configuration(cache=cache)
        if MODE in general_configuration:
            mode = general_configuration[MODE].upper()
            try:
                configuration.default_mode = RunnerMode[mode]
            except KeyError as error:
                raise InvalidConfiguration(
                    f"Got unexpected runner mode in configuration: {mode}"
                ) from error
        if CONTEXTS in statue_config_dict:
            configuration.contexts_repository.update_from_config(
                statue_config_dict[CONTEXTS]
            )
        if SOURCES in statue_config_dict:
            configuration.sources_repository.update_from_config(
                config=statue_config_dict[SOURCES],
                contexts_repository=configuration.contexts_repository,
            )
        if COMMANDS in statue_config_dict:
            configuration.commands_repository.update_from_config(
                statue_config_dict[COMMANDS]
            )
        return configuration

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
