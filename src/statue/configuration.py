"""Get Statue global configuration."""
from copy import deepcopy
from pathlib import Path
from typing import Any, List, MutableMapping, Optional

import toml

import statue.constants as consts
from statue.command import Command
from statue.excptions import EmptyConfiguration, InvalidCommand, UnknownCommand

__all__ = ["Configuration"]


class __ConfigurationMetaclass:  # pylint: disable=invalid-name

    __default_configuration: Optional[MutableMapping[str, Any]] = None
    __statue_configuration: Optional[MutableMapping[str, Any]] = None

    @property
    def default_configuration(self) -> Optional[MutableMapping[str, Any]]:
        """Getter of default configuration."""
        if self.__default_configuration is None:
            self.__load_default_configuration()
        return deepcopy(self.__default_configuration)

    @default_configuration.setter
    def default_configuration(
        self, default_configuration: Optional[MutableMapping[str, Any]]
    ) -> None:
        """Setter of default configuration."""
        self.__default_configuration = default_configuration

    @property
    def statue_configuration(self) -> MutableMapping[str, Any]:
        """Getter of general statue configuration."""
        if self.__statue_configuration is not None:
            return deepcopy(self.__statue_configuration)
        if self.default_configuration is not None:
            return self.default_configuration
        raise EmptyConfiguration()

    @statue_configuration.setter
    def statue_configuration(
        self, statue_configuration: Optional[MutableMapping[str, Any]]
    ) -> None:
        """Setter of general statue configuration."""
        self.__statue_configuration = statue_configuration

    @property
    def commands_configuration(self) -> Optional[MutableMapping[str, Any]]:
        """Getter of the commands configuration."""
        return self.statue_configuration.get(consts.COMMANDS, None)

    @property
    def commands_names_list(self) -> List[str]:
        """Getter of the commands list."""
        if self.commands_configuration is None:
            return []
        return list(self.commands_configuration.keys())

    @property
    def sources_configuration(self) -> Optional[MutableMapping[str, Any]]:
        """Getter of the sources configuration."""
        return self.statue_configuration.get(consts.SOURCES, None)

    @property
    def contexts_configuration(self) -> Optional[MutableMapping[str, Any]]:
        """Getter of the contexts configuration."""
        return self.statue_configuration.get(consts.CONTEXTS, None)

    def read_commands(
        self,
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
        for command_name in Configuration.commands_names_list:
            try:
                commands.append(
                    self.read_command(
                        command_name=command_name,
                        contexts=contexts,
                        allow_list=allow_list,
                        deny_list=deny_list,
                    )
                )
            except InvalidCommand:
                continue
        return commands

    def read_command(
        self,
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
        commands_configuration = self.commands_configuration
        if commands_configuration is None:
            raise UnknownCommand(command_name)
        command_setups = commands_configuration.get(command_name, None)
        if command_setups is None:
            raise UnknownCommand(command_name)
        if not self.__is_command_matching(
            command_name, command_setups, contexts, allow_list, deny_list
        ):
            raise InvalidCommand(
                command_name=command_name,
                contexts=contexts,
                allow_list=allow_list,
                deny_list=deny_list,
            )
        return Command(
            name=command_name,
            args=self.__read_commands_args(command_setups, contexts=contexts),
            help=command_setups[consts.HELP],
        )

    def load_configuration(
        self,
        statue_configuration_path: Path,
    ) -> None:
        """
        Load statue configuration.

        This method combines default configuration with user-defined configuration, read
        from configuration file.

        :param statue_configuration_path: User-defined file path containing
        repository-specific configurations
        """
        self.statue_configuration = self.__build_configuration(  # type: ignore
            statue_configuration_path
        )

    def reset_configuration(self) -> None:
        """Reset the general statue configuration."""
        self.default_configuration = None
        self.statue_configuration = None  # type: ignore

    def __load_default_configuration(self) -> None:
        if not consts.DEFAULT_CONFIGURATION_FILE.exists():
            return
        self.default_configuration = toml.load(consts.DEFAULT_CONFIGURATION_FILE)

    def __build_configuration(
        self,
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
        if self.default_configuration is None:
            return statue_config
        general_settings = statue_config.get(consts.STATUE, None)
        if general_settings is not None and general_settings.get(
            consts.OVERRIDE, False
        ):
            return statue_config
        statue_config[consts.COMMANDS] = self.default_configuration.get(
            consts.COMMANDS, {}
        )
        statue_config[consts.CONTEXTS] = self.default_configuration.get(
            consts.CONTEXTS, {}
        )
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
            return setups.get(consts.STANDARD, True)
        for command_context in contexts:
            if not setups.get(command_context, False):
                return False
        return True

    @classmethod
    def __read_commands_args(
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


Configuration = __ConfigurationMetaclass()
