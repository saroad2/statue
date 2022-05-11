"""Place for saving all available command builders."""
from collections import OrderedDict
from typing import Any, Dict, Iterator, List
from typing import OrderedDict as OrderedDictType

from statue.command_builder import CommandBuilder
from statue.config.contexts_repository import ContextsRepository
from statue.exceptions import UnknownCommand


class CommandsRepository:
    """Repository class for saving and accessing command builders."""

    def __init__(self, *command_builders: CommandBuilder):
        """
        Constructor.

        :param command_builders: Initial command builders to be saved
        :type command_builders: Context
        """
        self.command_builders_map: Dict[str, CommandBuilder] = {}
        self.add_command_builders(*command_builders)

    def __len__(self) -> int:
        """
        Number of available commands.

        :return: Number of commands
        :rtype: int
        """
        return len(self.command_builders_map)

    def __iter__(self) -> Iterator[CommandBuilder]:
        """
        Iterate over all available command builders.

        :return: Command builder iterator
        :rtype: Iterator[CommandBuilder]
        """
        return iter(self.command_builders_map.values())

    def __getitem__(self, item: str) -> CommandBuilder:
        """
        Get command builder by name or alias.

        :param item: Command name to be retrieved
        :type item: str
        :return: Command builder with given name
        :rtype: CommandBuilder
        :raises UnknownCommand: Raised when command is not found
        """
        if item in self:
            return self.command_builders_map[item]
        raise UnknownCommand(command_name=item)

    def __contains__(self, item) -> bool:
        """
        Does command builder available in repository.

        :param item: Command name to be searched
        :type item: str
        :return: does the command exist in repository
        :rtype: bool
        """
        return item in self.command_builders_map

    @property
    def command_names_list(self) -> List[str]:
        """Names of all available commands."""
        return list(self.command_builders_map.keys())

    def add_command_builders(self, *command_builders: CommandBuilder):
        """
        Add command builders to repository.

        :param command_builders: Command builder to be added to the
            repository
        :type command_builders: CommandBuilder
        """
        for command_builder in command_builders:
            self.command_builders_map[command_builder.name] = command_builder

    def remove_command_builder(self, command_builder: CommandBuilder):
        """
        Remove a command builder from repository.

        :param command_builder: Command builder to be removed.
        :type command_builder: CommandBuilder
        """
        del self.command_builders_map[command_builder.name]

    def reset(self):
        """Clear repository from all command builders."""
        self.command_builders_map.clear()

    def as_dict(self) -> OrderedDictType[str, Any]:
        """
        Encode commands repository as a dictionary.

        This is used in order to serialize the commands repository in
        a configuration file.

        :return: Serialized representation dictionary
        :rtype: OrderedDict[str, Any]
        """
        command_builders_list = list(self)
        command_builders_list.sort(key=lambda commands_builder: commands_builder.name)
        return OrderedDict(
            [
                (command_builder.name, command_builder.as_dict())
                for command_builder in command_builders_list
            ]
        )

    @classmethod
    def from_dict(
        cls, config: Dict[str, Any], contexts_repository: ContextsRepository
    ) -> "CommandsRepository":
        """
        Create commands repository from given configuration.

        :param config: Configuration to update repository from
        :type config: Dict[str, Any]
        :param contexts_repository: Contexts repository to get contexts from
        :type contexts_repository: ContextsRepository
        :return: Commands repository as described in configuration
        :rtype: CommandsRepository
        """
        builders = [
            CommandBuilder.from_dict(
                command_name=command_name,
                builder_setups=builder_setups,
                contexts_repository=contexts_repository,
            )
            for command_name, builder_setups in config.items()
        ]
        return CommandsRepository(*builders)
