"""Get Statue global configuration."""
from pathlib import Path
from typing import Any, List, MutableMapping, Optional

import toml

from statue.command import Command
from statue.commands_filter import CommandsFilter
from statue.commands_map import CommandsMap
from statue.config.commands_repository import CommandsRepository
from statue.config.contexts_repository import ContextsRepository
from statue.config.sources_repository import SourcesRepository
from statue.constants import COMMANDS, CONTEXTS, OVERRIDE, SOURCES, STATUE


class Configuration:
    """Configuration singleton for statue."""

    contexts_repository = ContextsRepository()
    sources_repository = SourcesRepository()
    commands_repository = CommandsRepository()

    @classmethod
    def default_configuration_path(cls) -> Path:
        """
        Get default configuration path.

        :return: Default configuration path
        :rtype: Path
        """
        return Path(__file__).parent.parent / "resources" / "defaults.toml"

    @classmethod
    def configuration_path(cls, directory: Path) -> Path:
        """
        Search for configuration file in directory.

        :param directory: Directory in which the configuration path is supposed to be
        :type directory: Path
        :return: Configuration path location
        :rtype: Path
        """
        return directory / "statue.toml"

    @classmethod
    def build_commands_map(
        cls, sources: List[Path], commands_filter: CommandsFilter
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
            commands_map[str(source)] = cls.build_commands(
                CommandsFilter.merge(commands_filter, cls.sources_repository[source])
            )
        return commands_map

    @classmethod
    def build_commands(cls, commands_filter: CommandsFilter) -> List[Command]:
        """
        Read commands with given constraints.

        :param commands_filter: Filter to choose commands according to.
        :type commands_filter: CommandsFilter
        :return: List of commands according to constraints
        :rtype: List[Command]
        """
        return [
            command_builder.build_command(*commands_filter.contexts)
            for command_builder in cls.commands_repository
            if commands_filter.pass_filter(command_builder)
        ]

    @classmethod
    def load_from_configuration_file(
        cls,
        statue_configuration_path: Optional[Path] = None,
    ):
        """
        Load statue configuration.

        This method combines default configuration with user-defined configuration, read
        from configuration file.

        :param statue_configuration_path: User-defined file path containing
            repository-specific configurations
        :type statue_configuration_path: None, str or Path
        """
        if statue_configuration_path is None:
            statue_configuration_path = cls.configuration_path(Path.cwd())
        if not statue_configuration_path.exists():
            return
        statue_config = toml.load(statue_configuration_path)
        general_settings = statue_config.get(STATUE, None)
        if general_settings is None or general_settings.get(OVERRIDE, False):
            default_configuration_path = cls.default_configuration_path()
            if default_configuration_path.exists():
                cls.update_from_config(toml.load(default_configuration_path))
        cls.update_from_config(statue_config)

    @classmethod
    def update_from_config(cls, statue_config: MutableMapping[str, Any]):
        """
        Update configuration from a loaded config map.

        :param statue_config: Configuration map as loaded from config file
        :type statue_config: MutableMapping[str, Any]
        """
        if CONTEXTS in statue_config:
            cls.contexts_repository.update_from_config(statue_config[CONTEXTS])
        if SOURCES in statue_config:
            cls.sources_repository.update_from_config(
                config=statue_config[SOURCES],
                contexts_repository=cls.contexts_repository,
            )
        if COMMANDS in statue_config:
            cls.commands_repository.update_from_config(statue_config[COMMANDS])

    @classmethod
    def reset_configuration(cls) -> None:
        """Reset the general statue configuration."""
        cls.contexts_repository.reset()
        cls.sources_repository.reset()
        cls.commands_repository.reset()
