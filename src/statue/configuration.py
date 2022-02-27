"""Get Statue global configuration."""
from copy import deepcopy
from pathlib import Path
from typing import Any, List, MutableMapping, Optional, Union

import toml

from statue.command import Command
from statue.command_builder import CommandBuilder
from statue.constants import (
    COMMANDS,
    CONTEXTS,
    DEFAULT_CONFIGURATION_FILE,
    OVERRIDE,
    SOURCES,
    STATUE,
)
from statue.contexts_repository import ContextsRepository
from statue.exceptions import (
    EmptyConfiguration,
    InvalidCommand,
    MissingConfiguration,
    UnknownCommand,
)


class Configuration:
    """Configuration singleton for statue."""

    __default_configuration: Optional[MutableMapping[str, Any]] = None
    __statue_configuration: Optional[MutableMapping[str, Any]] = None
    contexts_repository = ContextsRepository()

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
    def commands_names_list(cls) -> List[str]:
        """
        List of all available commands.

        :return: Available commands list
        :rtype: List[str]
        """
        commands_configuration = cls.commands_configuration()
        if commands_configuration is None:
            return []
        return list(commands_configuration.keys())

    @classmethod
    def get_command_builder(cls, command_name: str) -> Optional[CommandBuilder]:
        """
        Get configuration dictionary of a context.

        :param command_name: Name of the desired command.
        :type command_name: str
        :return: configuration dictionary.
        :rtype: None or mutable mapping
        :raises MissingConfiguration: raised when no contexts configuration was set.
        """
        commands_configuration = cls.commands_configuration()
        if commands_configuration is None:
            raise MissingConfiguration(COMMANDS)
        return commands_configuration.get(command_name, None)

    @classmethod
    def sources_configuration(
        cls,
    ) -> MutableMapping[Path, MutableMapping[str, Any]]:
        """
        Getter of the sources configuration.

        :return: Sources configuration dictionary
        :rtype: MutableMapping[str, Any]
        :raises MissingConfiguration: raised if no sources configuration was set.
        """
        sources_configuration: Optional[
            MutableMapping[Path, MutableMapping[str, Any]]
        ] = cls.statue_configuration().get(SOURCES, None)
        if sources_configuration is None:
            raise MissingConfiguration(SOURCES)
        return sources_configuration

    @classmethod
    def sources_list(cls) -> List[Path]:
        """
        List of sources to run statue over, as specified in the configuration file.

        :return: Available sources list
        :rtype: List[Path]
        """
        return list(cls.sources_configuration().keys())

    @classmethod
    def get_source_configuration(
        cls, source: Union[Path, str]
    ) -> Optional[MutableMapping[str, Any]]:
        """
        Get configuration dictionary of a context.

        :param source: Name of the desired source.
        :type source: str
        :return: configuration dictionary.
        :rtype: None or mutable mapping
        """
        sources_configuration = cls.sources_configuration()
        if not isinstance(source, Path):
            source = Path(source)
        for source_path, setup in sources_configuration.items():
            try:
                source.relative_to(source_path)
                return setup
            except ValueError:
                continue
        return None

    @classmethod
    def read_commands(
        cls,
        contexts: Optional[List[str]] = None,
        allow_list: Optional[List[str]] = None,
        deny_list: Optional[List[str]] = None,
    ) -> List[Command]:
        """
        Read commands with given constraints.

        :param contexts: List of contexts to choose commands from.
        :type contexts: None or List[str]
        :param allow_list: List of allowed commands. If None, take all commands
        :type allow_list: None or List[str]
        :param deny_list: List of denied commands. If None, take all commands
        :type deny_list: None or List[str]
        :return: List of commands according to constraints
        :rtype: List[Command]
        """
        commands = []
        contexts = [] if contexts is None else contexts
        for command_name in cls.commands_names_list():
            try:
                commands.append(
                    cls.read_command(
                        command_name=command_name,
                        contexts=contexts,
                        allow_list=allow_list,
                        deny_list=deny_list,
                    )
                )
            except InvalidCommand:
                continue
        return commands

    @classmethod
    def read_command(
        cls,
        command_name: str,
        contexts: Optional[List[str]] = None,
        allow_list: Optional[List[str]] = None,
        deny_list: Optional[List[str]] = None,
    ) -> Command:
        """
        Read command with given constraints.

        :param command_name: Name of the command to read
        :type command_name: str
        :param contexts: List of contexts to choose commands from.
        :type contexts: None or List[str]
        :param allow_list: List of allowed commands. If None, take all commands
        :type allow_list: None or List[str]
        :param deny_list: List of denied commands. If None, take all commands
        :type deny_list: None or List[str]
        :return: Command instance with constraints
        :rtype: Command
        :raises UnknownCommand: raised if command is missing from settings file.
        :raises InvalidCommand: raised if command doesn't fit the given contexts,
            allow list or deny list
        """
        if (
            allow_list is not None
            and len(allow_list) != 0
            and command_name not in allow_list
        ):
            raise InvalidCommand(
                f'Command "{command_name}" '
                f"was not specified in allowed list: {', '.join(allow_list)}"
            )
        if deny_list is not None and command_name in deny_list:
            raise InvalidCommand(
                f'Command "{command_name}" '
                f"was explicitly denied in deny list: {', '.join(deny_list)}"
            )
        command_builder = cls.get_command_builder(command_name)
        if contexts is None:
            contexts = []
        if command_builder is None:
            raise UnknownCommand(command_name)
        contexts_objects = [
            cls.contexts_repository.get_context(context_identifier)
            for context_identifier in contexts
        ]
        return command_builder.build_command(*contexts_objects)

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
            statue_config[SOURCES] = {
                Path(source): setup for source, setup in statue_config[SOURCES].items()
            }
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
