"""Get Statue global configuration."""
import sys
from collections import OrderedDict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, FrozenSet, List, Optional
from typing import OrderedDict as OrderedDictType
from typing import TypeVar, Union

import tomli
import tomli_w

from statue.cache import Cache
from statue.command import Command
from statue.command_builder import CommandBuilder
from statue.commands_filter import CommandsFilter
from statue.commands_map import CommandsMap
from statue.config.commands_repository import CommandsRepository
from statue.config.contexts_repository import ContextsRepository
from statue.config.sources_repository import SourcesRepository
from statue.constants import (
    CACHE,
    COMMANDS,
    CONTEXTS,
    DEFAULT_HISTORY_SIZE,
    GENERAL,
    HISTORY_SIZE,
    MODE,
    SOURCES,
)
from statue.context import Context
from statue.exceptions import (
    InvalidConfiguration,
    MissingConfiguration,
    StatueConfigurationError,
)
from statue.runner import RunnerMode

if sys.version_info < (3, 9):  # pragma: no cover
    from importlib_resources.abc import Traversable
else:  # pragma: no cover
    from importlib.abc import Traversable


T = TypeVar("T")


@dataclass
class Configuration:
    """Configuration singleton for statue."""

    cache: Cache
    default_mode: RunnerMode = field(default=RunnerMode.DEFAULT_MODE)
    contexts_repository: ContextsRepository = field(default_factory=ContextsRepository)
    commands_repository: CommandsRepository = field(default_factory=CommandsRepository)
    sources_repository: SourcesRepository = field(default_factory=SourcesRepository)

    def remove_context(self, context: Context):
        """
        Remove all references of a context from the configuration.

        :param context: Context object to be removed
        :type context: Context
        """
        for source in self.sources_repository.sources_list:
            original_filter = self.sources_repository[source]
            self.sources_repository[source] = CommandsFilter(
                contexts=[
                    filter_context
                    for filter_context in original_filter.contexts
                    if filter_context != context
                ],
                allowed_commands=original_filter.allowed_commands,
                denied_commands=original_filter.denied_commands,
            )
        for command_builder in self.commands_repository:
            command_builder.remove_context(context)
        self.contexts_repository.remove_context(context)

    def remove_command(self, command_builder: CommandBuilder):
        """
        Remove all references of a command builder from the configuration.

        :param command_builder: Command builder to be removed
        :type command_builder: CommandBuilder
        """
        for source in self.sources_repository.sources_list:
            original_filter = self.sources_repository[source]
            self.sources_repository[source] = CommandsFilter(
                contexts=original_filter.contexts,
                allowed_commands=self._none_or_remove(
                    original_filter.allowed_commands, command_builder.name
                ),
                denied_commands=self._none_or_remove(
                    original_filter.denied_commands, command_builder.name
                ),
            )
        self.commands_repository.remove_command_builder(command_builder)

    def build_commands_map(
        self, sources: List[Path], commands_filter: CommandsFilter
    ) -> CommandsMap:
        """
        Build commands map from sources list and a commands filter.

        :param sources: Sources list of the commands map
        :type sources: List[Path]
        :param commands_filter: Base filter to choose commands with
        :type commands_filter: CommandsFilter
        :return: Commands map with sources as keys
        :rtype: CommandsMap
        """
        commands_map = CommandsMap()
        for source in sources:
            commands = self.build_commands(
                CommandsFilter.merge(commands_filter, self.sources_repository[source])
            )
            if len(commands) != 0:
                commands_map[source] = commands
        return commands_map

    def build_commands(self, commands_filter: CommandsFilter) -> List[Command]:
        """
        Read commands with given constraints.

        :param commands_filter: Filter to choose commands according to.
        :type commands_filter: CommandsFilter
        :return: List of commands according to constraints
        :rtype: List[Command]
        """
        return [
            command_builder.build_command(*commands_filter.contexts)
            for command_builder in self.commands_repository
            if commands_filter.pass_filter(command_builder)
        ]

    def as_dict(self) -> OrderedDictType[str, Any]:
        """
        Encode configuration as a dictionary.

        This is used in order to serialize the configuration to be later saved
        in a file.

        :return: Serialized representation dictionary
        :rtype: OrderedDict[str, Any]
        """
        general_dict = OrderedDict(
            [
                (MODE, self.default_mode.name.lower()),
                (HISTORY_SIZE, self.cache.history_size),
            ]
        )
        if not self.cache.enabled:
            general_dict[CACHE] = False
        return OrderedDict(
            [
                (GENERAL, general_dict),
                (CONTEXTS, self.contexts_repository.as_dict()),
                (COMMANDS, self.commands_repository.as_dict()),
                (SOURCES, self.sources_repository.as_dict()),
            ]
        )

    def to_toml(self, path: Path):
        """
        Save configuration to toml file.

        :param path: Path to save configuration in
        :type path: Path
        """
        with path.open(mode="wb") as configuration_file:
            tomli_w.dump(self.as_dict(), configuration_file)

    @classmethod
    def from_file(
        cls,
        config_path: Optional[Union[Path, Traversable]] = None,
        cache_dir: Optional[Path] = None,
    ) -> "Configuration":
        """
        Load statue configuration.

        This method combines default configuration with user-defined configuration, read
        from configuration file.

        :param config_path: User-defined file path containing
            repository-specific configurations
        :type config_path: Optional[Path]
        :param cache_dir: Optional Caching directory
        :type cache_dir: Optional[Path]
        :return: Configuration instance
        :rtype: Configuration
        :raises MissingConfiguration: Raised when could not load
        """
        if config_path is None:
            config_path = cls.configuration_path()
        if isinstance(config_path, Path) and not config_path.exists():
            raise MissingConfiguration()
        with config_path.open(mode="rb") as configuration_file:
            statue_config = tomli.load(configuration_file)
        cache_dir = cls.cache_path(Path.cwd()) if cache_dir is None else cache_dir
        return cls.from_dict(cache_dir=cache_dir, statue_config_dict=statue_config)

    @classmethod
    def from_dict(
        cls, cache_dir: Path, statue_config_dict: Dict[str, Any]
    ) -> "Configuration":
        """
        Build configuration from a loaded config map.

        :param cache_dir: Directory for keeping cache.
        :type cache_dir: Path
        :param statue_config_dict: Configuration map as loaded from config file
        :type statue_config_dict: Dict[str, Any]
        :return: Built configuration instance
        :type: Configuration
        :raises InvalidConfiguration: Raised when some fields are invalid
            in configuration
        """
        general_configuration = statue_config_dict.get(GENERAL, {})
        history_size = general_configuration.get(HISTORY_SIZE, DEFAULT_HISTORY_SIZE)
        cached_enabled = general_configuration.get(CACHE, True)
        cache = Cache(
            cache_root_directory=cache_dir, size=history_size, enabled=cached_enabled
        )
        mode = RunnerMode.DEFAULT_MODE
        if MODE in general_configuration:
            mode_string = general_configuration[MODE].upper()
            try:
                mode = RunnerMode[mode_string]
            except KeyError as error:
                raise InvalidConfiguration(
                    f"Got unexpected runner mode {mode_string}", location=[GENERAL]
                ) from error
        contexts_repository = cls.build_contexts_repository(statue_config_dict)
        commands_repository = cls.build_commands_repository(
            statue_config_dict, contexts_repository
        )
        sources_repository = SourcesRepository.from_dict(
            config=statue_config_dict.get(SOURCES, {}),
            contexts_repository=contexts_repository,
        )
        return Configuration(
            cache=cache,
            default_mode=mode,
            contexts_repository=contexts_repository,
            commands_repository=commands_repository,
            sources_repository=sources_repository,
        )

    @classmethod
    def build_contexts_repository(
        cls, statue_config_dict: Dict[str, Any]
    ) -> ContextsRepository:
        """
        Build contexts repository from configuration dictionary.

        :param statue_config_dict: Configuration map as loaded from config file
        :type statue_config_dict: Dict[str, Any]
        :return: Built contexts repository
        :rtype: ContextsRepository
        :raises StatueConfigurationError: General configuration-related error.
        """
        try:
            return ContextsRepository.from_dict(statue_config_dict.get(CONTEXTS, {}))
        except StatueConfigurationError as error:
            error.append_location_item(CONTEXTS)
            raise error

    @classmethod
    def build_commands_repository(
        cls, statue_config_dict: Dict[str, Any], contexts_repository: ContextsRepository
    ) -> CommandsRepository:
        """
        Build contexts repository from configuration dictionary.

        :param statue_config_dict: Configuration map as loaded from config file
        :type statue_config_dict: Dict[str, Any]
        :param contexts_repository: Contexts repository to get contexts from
        :type contexts_repository: ContextsRepository
        :return: Built contexts repository
        :rtype: CommandsRepository
        :raises StatueConfigurationError: General configuration-related error.
        """
        try:
            return CommandsRepository.from_dict(
                config=statue_config_dict.get(COMMANDS, {}),
                contexts_repository=contexts_repository,
            )
        except StatueConfigurationError as error:
            error.append_location_item(COMMANDS)
            raise error

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

    @classmethod
    def empty_configuration(cls) -> "Configuration":
        """
        Creates an empty configuration.

        :return: Empty configuration
        :rtype: Configuration
        """
        cache = Cache(size=DEFAULT_HISTORY_SIZE)
        return Configuration(cache=cache)

    @classmethod
    def _none_or_remove(
        cls, optional_set: Optional[FrozenSet[T]], removed_item: T
    ) -> Optional[FrozenSet[T]]:
        if optional_set is None:
            return None
        return frozenset(item for item in optional_set if item != removed_item)
