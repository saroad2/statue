"""Get Statue global configuration."""
from collections import OrderedDict
from pathlib import Path
from typing import Any, List
from typing import OrderedDict as OrderedDictType

import tomli_w

from statue.cache import Cache
from statue.command import Command
from statue.commands_filter import CommandsFilter
from statue.commands_map import CommandsMap
from statue.config.commands_repository import CommandsRepository
from statue.config.contexts_repository import ContextsRepository
from statue.config.sources_repository import SourcesRepository
from statue.constants import COMMANDS, CONTEXTS, GENERAL, HISTORY_SIZE, MODE, SOURCES
from statue.runner import RunnerMode


class Configuration:
    """Configuration singleton for statue."""

    def __init__(
        self,
        cache: Cache,
        default_mode: RunnerMode = RunnerMode.SYNC,
    ):
        """
        Initialize configuration.

        :param default_mode: Default mode for evaluation runner
        :type default_mode: RunnerMode
        :param cache: Cache instance for saving evaluations
        :type cache: Cache
        """
        self.cache = cache
        self.contexts_repository = ContextsRepository()
        self.sources_repository = SourcesRepository()
        self.commands_repository = CommandsRepository()
        self.default_mode = default_mode

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
