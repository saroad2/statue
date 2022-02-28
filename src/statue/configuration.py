"""Get Statue global configuration."""
from copy import deepcopy
from pathlib import Path
from typing import Any, List, MutableMapping, Optional, Union

import toml

from statue.command import Command
from statue.command_builder import CommandBuilder
from statue.commands_filter import CommandsFilter
from statue.commands_map import CommandsMap
from statue.constants import (
    COMMANDS,
    CONTEXTS,
    DEFAULT_CONFIGURATION_FILE,
    OVERRIDE,
    SOURCES,
    STATUE,
)
from statue.contexts_repository import ContextsRepository
from statue.exceptions import EmptyConfiguration, MissingConfiguration, UnknownCommand
from statue.sources_repository import SourcesRepository


class Configuration:
    """Configuration singleton for statue."""

    __default_configuration: Optional[MutableMapping[str, Any]] = None
    __statue_configuration: Optional[MutableMapping[str, Any]] = None
    contexts_repository = ContextsRepository()
    sources_repository = SourcesRepository()

    @classmethod
    def configuration_path(cls, directory: Union[Path, str]) -> Path:
        """
        Get default path of configuration file in directory.

        :param directory: Directory in which the configuration path is supposed to be
        :type directory: Path or str
        :return: Configuration path location
        :rtype: Path
        """
        if isinstance(directory, str):
            directory = Path(directory)
        return directory / "statue.toml"

    @classmethod
    def default_configuration(cls) -> Optional[MutableMapping[str, Any]]:
        """
        Default configuration path.

        :return: Default configuration path location
        :rtype: Path
        """
        if cls.__default_configuration is None:
            cls.__load_default_configuration()
        return deepcopy(cls.__default_configuration)

    @classmethod
    def set_default_configuration(
        cls, default_configuration: Optional[MutableMapping[str, Any]]
    ) -> None:
        """
        Setter of default configuration.

        :param default_configuration: Configuration to be saved
        :type default_configuration: None or mutable mapping
        """
        cls.__default_configuration = default_configuration

    @classmethod
    def statue_configuration(cls) -> MutableMapping[str, Any]:
        """
        Getter of general statue configuration.

        If not set, take default configuration instead.

        :return: Configuration dictionary of Statue
        :rtype: MutableMapping[str, Any]
        :raises EmptyConfiguration: Raised if no configuration was set.
        """
        if cls.__statue_configuration is not None:
            return deepcopy(cls.__statue_configuration)
        default_configuration = cls.default_configuration()
        if default_configuration is not None:
            return default_configuration
        raise EmptyConfiguration()

    @classmethod
    def set_statue_configuration(
        cls, statue_configuration: Optional[MutableMapping[str, Any]]
    ) -> None:
        """
        Setter of general statue configuration.

        :param statue_configuration: Configuration to be saved
        :type statue_configuration: None or mutable mapping
        """
        cls.__statue_configuration = statue_configuration

    @classmethod
    def commands_configuration(cls) -> Optional[MutableMapping[str, CommandBuilder]]:
        """
        Getter of the commands configuration.

        :return: Commands configuration dictionary
        :rtype: MutableMapping[str, Any]
        """
        return cls.statue_configuration().get(COMMANDS, None)

    @classmethod
    def command_names_list(cls) -> List[str]:
        """
        List of names of all available commands.

        :return: Available commands list
        :rtype: List[str]
        """
        commands_configuration = cls.commands_configuration()
        if commands_configuration is None:
            return []
        return list(commands_configuration.keys())

    @classmethod
    def command_builders_list(cls) -> List[CommandBuilder]:
        """
        List of all available commands builders.

        :return: Available commands list
        :rtype: List[CommandBuilder]
        """
        commands_configuration = cls.commands_configuration()
        if commands_configuration is None:
            return []
        return list(commands_configuration.values())

    @classmethod
    def get_command_builder(cls, command_name: str) -> CommandBuilder:
        """
        Get configuration dictionary of a context.

        :param command_name: Name of the desired command.
        :type command_name: str
        :return: Command builder with given name
        :rtype: CommandBuilder
        :raises MissingConfiguration: Raised when no command configuration was set.
        :raises UnknownCommand: Raised when no command was found with given name.
        """
        commands_configuration = cls.commands_configuration()
        if commands_configuration is None:
            raise MissingConfiguration(COMMANDS)
        if command_name not in commands_configuration:
            raise UnknownCommand(command_name)
        return commands_configuration[command_name]

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
            for command_builder in cls.command_builders_list()
            if commands_filter.pass_filter(command_builder)
        ]

    @classmethod
    def load_configuration(
        cls,
        statue_configuration_path: Optional[Union[str, Path]] = None,
    ) -> None:
        """
        Load statue configuration.

        This method combines default configuration with user-defined configuration, read
        from configuration file.

        :param statue_configuration_path: User-defined file path containing
            repository-specific configurations
        :type statue_configuration_path: None, str or Path
        """
        if statue_configuration_path is None:
            cwd = Path.cwd()
            statue_configuration_path = cls.configuration_path(cwd)
        if isinstance(statue_configuration_path, str):
            statue_configuration_path = Path(statue_configuration_path)
        cls.set_statue_configuration(
            cls.__build_configuration(statue_configuration_path)
        )

    @classmethod
    def reset_configuration(cls) -> None:
        """Reset the general statue configuration."""
        cls.set_default_configuration(None)
        cls.set_statue_configuration(None)
        cls.contexts_repository.reset()
        cls.sources_repository.reset()

    @classmethod
    def __load_default_configuration(cls) -> None:
        if not DEFAULT_CONFIGURATION_FILE.exists():
            return
        default_configuration = toml.load(DEFAULT_CONFIGURATION_FILE)
        if CONTEXTS in default_configuration:
            cls.contexts_repository.update_from_config(default_configuration[CONTEXTS])
        if COMMANDS in default_configuration:
            default_configuration[COMMANDS] = {
                command_name: CommandBuilder.from_json(
                    command_name=command_name,
                    builder_setups=command_instructions,
                )
                for command_name, command_instructions in default_configuration[
                    COMMANDS
                ].items()
            }
        cls.set_default_configuration(default_configuration)

    @classmethod
    def __build_configuration(
        cls,
        statue_configuration_path: Path,
    ) -> Optional[MutableMapping[str, Any]]:
        """
        Build statue configuration.

        This method combines default configuration with user-defined configuration, read
        from configuration file.

        :param statue_configuration_path: User-defined file path containing
            repository-specific configurations
        :type statue_configuration_path: Path
        :return: Configuration mutable map
        :rtype: None or MutableMapping[str, Any]
        """
        if not statue_configuration_path.exists():
            return None
        statue_config = toml.load(statue_configuration_path)
        default_configuration = cls.default_configuration()
        if default_configuration is None:
            return statue_config
        general_settings = statue_config.get(STATUE, None)
        if general_settings is not None and general_settings.get(OVERRIDE, False):
            return statue_config
        commands_configuration = cls.__build_commands_configuration(
            statue_commands_configuration=statue_config.get(COMMANDS, None),
            default_commands_configuration=default_configuration.get(COMMANDS, None),
        )
        if commands_configuration is not None:
            statue_config[COMMANDS] = commands_configuration
        if CONTEXTS in statue_config:
            cls.contexts_repository.update_from_config(statue_config[CONTEXTS])
        if SOURCES in statue_config:
            cls.sources_repository.update_from_config(
                config=statue_config[SOURCES],
                contexts_repository=cls.contexts_repository,
            )
        return statue_config

    @classmethod
    def __build_commands_configuration(
        cls,
        statue_commands_configuration: Optional[MutableMapping[str, Any]],
        default_commands_configuration: Optional[MutableMapping[str, CommandBuilder]],
    ) -> Optional[MutableMapping[str, Any]]:
        if statue_commands_configuration is None:
            return default_commands_configuration
        if default_commands_configuration is None:
            return statue_commands_configuration
        commands_configuration = deepcopy(default_commands_configuration)
        for command_name, command_setups in statue_commands_configuration.items():
            if command_name in commands_configuration:
                commands_configuration[command_name].update_from_config(command_setups)
            else:
                commands_configuration[command_name] = CommandBuilder.from_json(
                    command_name=command_name, builder_setups=command_setups
                )
        return commands_configuration
