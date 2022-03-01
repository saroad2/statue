"""Place for saving all available command builders."""
from typing import Any, Dict, Iterator, List, MutableMapping

from statue.command_builder import CommandBuilder
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
        if self.has_command(item):
            return self.command_builders_map[item]
        raise UnknownCommand(command_name=item)

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

    def has_command(self, command_name: str) -> bool:
        """
        Does command builder available in repository.

        :param command_name: Command name to be searched
        :type command_name: str
        :return: does the command exist in repository
        :rtype: bool
        """
        return command_name in self.command_builders_map

    def reset(self):
        """Clear repository from all command builders."""
        self.command_builders_map.clear()

    def update_from_config(self, config: MutableMapping[str, Any]):
        """
        Update commands repository from given configuration.

        :param config: Configuration to update repository from
        :type config: MutableMapping[str, Any]
        """
        for command_name, builder_setups in config.items():
            if self.has_command(command_name):
                self[command_name].update_from_config(builder_setups)
            else:
                self.add_command_builders(
                    CommandBuilder.from_config(
                        command_name=command_name, builder_setups=builder_setups
                    )
                )
