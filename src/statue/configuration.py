"""Get Statue global configuration."""
from copy import deepcopy
from pathlib import Path
from typing import Any, List, MutableMapping, Optional

import toml

import statue.constants as consts
from statue.command import Command
from statue.excptions import (
    EmptyConfiguration,
    InvalidCommand,
    MissingConfiguration,
    UnknownCommand,
    UnknownContext,
)


class Configuration:
    """Configuration singleton for statue."""

    __default_configuration: Optional[MutableMapping[str, Any]] = None
    __statue_configuration: Optional[MutableMapping[str, Any]] = None

    @classmethod
    def default_configuration(cls) -> Optional[MutableMapping[str, Any]]:
        """Getter of default configuration."""
        if cls.__default_configuration is None:
            cls.__load_default_configuration()
        return deepcopy(cls.__default_configuration)

    @classmethod
    def set_default_configuration(
        cls, default_configuration: Optional[MutableMapping[str, Any]]
    ) -> None:
        """Setter of default configuration."""
        cls.__default_configuration = default_configuration

    @classmethod
    def statue_configuration(cls) -> MutableMapping[str, Any]:
        """Getter of general statue configuration."""
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
        """Setter of general statue configuration."""
        cls.__statue_configuration = statue_configuration

    @classmethod
    def commands_configuration(cls) -> Optional[MutableMapping[str, Any]]:
        """Getter of the commands configuration."""
        return cls.statue_configuration().get(consts.COMMANDS, None)

    @classmethod
    def commands_names_list(cls) -> List[str]:
        """Getter of the commands list."""
        commands_configuration = cls.commands_configuration()
        if commands_configuration is None:
            return []
        return list(commands_configuration.keys())

    @classmethod
    def get_command_configuration(
        cls, command_name: str
    ) -> Optional[MutableMapping[str, Any]]:
        """
        Get configuration dictionary of a context.

        :param command_name: Name of the desired command.
        :type command_name: str
        :return: configuration dictionary.
        :raises: raise :Class:`MissingConfiguration` if no contexts configuration was
        set.
        """
        commands_configuration = cls.commands_configuration()
        if commands_configuration is None:
            raise MissingConfiguration(consts.COMMANDS)
        return commands_configuration.get(command_name, None)

    @classmethod
    def sources_configuration(cls) -> Optional[MutableMapping[str, Any]]:
        """Getter of the sources configuration."""
        return cls.statue_configuration().get(consts.SOURCES, None)

    @classmethod
    def sources_list(cls) -> List[str]:
        """Getter of the sources configuration."""
        sources_configuration = cls.sources_configuration()
        if sources_configuration is None:
            return []
        return list(sources_configuration.keys())

    @classmethod
    def get_source_configuration(
        cls, source: str
    ) -> Optional[MutableMapping[str, Any]]:
        """
        Get configuration dictionary of a context.

        :param source: Name of the desired context.
        :type source: str
        :return: configuration dictionary.
        :raises: raise :Class:`MissingConfiguration` if no contexts configuration was
        set.
        """
        sources_configuration = cls.sources_configuration()
        if sources_configuration is None:
            raise MissingConfiguration(consts.CONTEXTS)
        return sources_configuration.get(source, None)

    @classmethod
    def contexts_configuration(cls) -> Optional[MutableMapping[str, Any]]:
        """Getter of the contexts configuration."""
        return cls.statue_configuration().get(consts.CONTEXTS, None)

    @classmethod
    def get_context_configuration(
        cls, context_name: str
    ) -> Optional[MutableMapping[str, Any]]:
        """
        Get configuration dictionary of a context.

        :param context_name: Name of the desired context.
        :type context_name: str
        :return: configuration dictionary.
        :raises: raise :Class:`MissingConfiguration` if no contexts configuration was
        set.
        """
        contexts_configuration = cls.contexts_configuration()
        if contexts_configuration is None:
            raise MissingConfiguration(consts.CONTEXTS)
        return contexts_configuration.get(context_name, None)

    @classmethod
    def read_commands(
        cls,
        contexts: Optional[List[str]] = None,
        allow_list: Optional[List[str]] = None,
        deny_list: Optional[List[str]] = None,
    ) -> List[Command]:
        """
        Read commands from a settings file.

        :param contexts: List of str. a list of contexts to choose commands from.
        :param allow_list: List of allowed commands. If None, take all commands
        :param deny_list: List of denied commands. If None, take all commands
        :return: a list of :class:`Command`
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
        Read command from a settings file.

        :param command_name: the name of the command to read.
        :param contexts: List of str. a list of contexts to choose commands from.
        :param allow_list: List of allowed commands. If None, take all commands
        :param deny_list: List of denied commands. If None, take all commands
        :return: a :class:`Command` instance
        :raises: :class:`UnknownCommand` if command is missing from settings file.
        :class:`InvalidCommand` of command doesn't fit the given contexts, allow list
         and deny list
        """
        command_configuration = cls.get_command_configuration(command_name)
        if command_configuration is None:
            raise UnknownCommand(command_name)
        if not cls.__is_command_matching(
            command_name, command_configuration, contexts, allow_list, deny_list
        ):
            raise InvalidCommand(
                command_name=command_name,
                contexts=contexts,
                allow_list=allow_list,
                deny_list=deny_list,
            )
        return Command(
            name=command_name,
            args=cls.__read_command_args(command_configuration, contexts=contexts),
            help=command_configuration[consts.HELP],
        )

    @classmethod
    def load_configuration(
        cls,
        statue_configuration_path: Path,
    ) -> None:
        """
        Load statue configuration.

        This method combines default configuration with user-defined configuration, read
        from configuration file.

        :param statue_configuration_path: User-defined file path containing
        repository-specific configurations
        """
        cls.set_statue_configuration(
            cls.__build_configuration(statue_configuration_path)
        )

    @classmethod
    def reset_configuration(cls) -> None:
        """Reset the general statue configuration."""
        cls.set_default_configuration(None)
        cls.set_statue_configuration(None)

    @classmethod
    def __load_default_configuration(cls) -> None:
        if not consts.DEFAULT_CONFIGURATION_FILE.exists():
            return
        cls.set_default_configuration(toml.load(consts.DEFAULT_CONFIGURATION_FILE))

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
        """
        if not statue_configuration_path.exists():
            return None
        statue_config = toml.load(statue_configuration_path)
        default_configuration = cls.default_configuration()
        if default_configuration is None:
            return statue_config
        general_settings = statue_config.get(consts.STATUE, None)
        if general_settings is not None and general_settings.get(
            consts.OVERRIDE, False
        ):
            return statue_config
        statue_config[consts.COMMANDS] = default_configuration.get(consts.COMMANDS, {})
        statue_config[consts.CONTEXTS] = default_configuration.get(consts.CONTEXTS, {})
        return statue_config

    @classmethod
    def __is_command_matching(  # pylint: disable=too-many-arguments
        cls,
        command_name: str,
        setups: MutableMapping[str, Any],
        contexts: Optional[List[str]],
        allow_list: Optional[List[str]],
        deny_list: Optional[List[str]],
    ) -> bool:
        """
        Check whether a command fits the restrictions or not.

        :param command_name: the name of the command to read.
        :param setups: Dictionary. The command's configuration.
        :param contexts: List of str. a list of contexts.
        :param allow_list: List of allowed commands.
        :param deny_list: List of denied commands.
        :return: Boolean. Does the command fit the restrictions
        """
        if deny_list is not None and command_name in deny_list:
            return False
        if (
            allow_list is not None
            and len(allow_list) != 0  # noqa: W503
            and command_name not in allow_list  # noqa: W503
        ):
            return False
        if contexts is None or len(contexts) == 0:
            return cls.__command_match_default_context(setups)
        for command_context in contexts:
            if not cls.__command_match_context(setups, command_context):
                return False
        return True

    @classmethod
    def __command_match_context(
        cls, setups: MutableMapping[str, Any], context_name: str
    ) -> bool:
        if context_name == consts.STANDARD:
            return cls.__command_match_default_context(setups)
        context_configuration = cls.get_context_configuration(context_name)
        if context_configuration is None:
            raise UnknownContext(context_name)
        if setups.get(context_name, False):
            return True
        parent_context = context_configuration.get(consts.PARENT, None)
        if parent_context is not None:
            return cls.__command_match_context(setups, parent_context)
        return False

    @classmethod
    def __command_match_default_context(cls, setups: MutableMapping[str, Any]) -> bool:
        return setups.get(consts.STANDARD, True)

    @classmethod
    def __read_command_args(
        cls, setups: MutableMapping[str, Any], contexts: Optional[List[str]]
    ) -> List[str]:
        base_args = list(setups.get(consts.ARGS, []))
        if contexts is None:
            return base_args
        for command_context in contexts:
            context_obj = setups.get(command_context, None)
            if not isinstance(context_obj, dict):
                continue
            args: List[str] = context_obj.get(consts.ARGS, None)
            if args is not None:
                return args
            add_args = context_obj.get(consts.ADD_ARGS, None)
            if add_args is not None:
                base_args.extend(add_args)
            clear_args = context_obj.get(consts.CLEAR_ARGS, False)
            if clear_args:
                return []
        return base_args
