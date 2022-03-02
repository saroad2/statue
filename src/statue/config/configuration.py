"""Get Statue global configuration."""
from pathlib import Path
from typing import List

from statue.command import Command
from statue.commands_filter import CommandsFilter
from statue.commands_map import CommandsMap
from statue.config.commands_repository import CommandsRepository
from statue.config.contexts_repository import ContextsRepository
from statue.config.sources_repository import SourcesRepository


class Configuration:
    """Configuration singleton for statue."""

    def __init__(self):
        """Initialize configuration."""
        self.contexts_repository = ContextsRepository()
        self.sources_repository = SourcesRepository()
        self.commands_repository = CommandsRepository()

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
                commands_map[str(source)] = commands
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
