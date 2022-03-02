"""Place for saving all available sources with default commands filter."""
from pathlib import Path
from typing import Any, Dict, List, MutableMapping

from statue.commands_filter import CommandsFilter
from statue.config.contexts_repository import ContextsRepository
from statue.constants import ALLOW_LIST, CONTEXTS, DENY_LIST


class SourcesRepository:
    """
    Repository class for saving and accessing sources.

    This is done in order to get specific commands filter from each source.
    """

    def __init__(self):
        """Initialize repository."""
        self.sources_filters_map: Dict[Path, CommandsFilter] = {}

    def __len__(self) -> int:
        """
        Number of available sources commands filters.

        :return: Number of sources commands filters
        :rtype: int
        """
        return len(self.sources_filters_map)

    def __setitem__(self, key: Path, value: CommandsFilter):
        """
        Set a commands filter for a given source.

        :param key: Source to save commands filter for
        :type key: Path
        :param value: Command filter for given source
        :type value: CommandsFilter
        """
        self.sources_filters_map[key] = value

    def __getitem__(self, item: Path) -> CommandsFilter:
        """
        Get a commands filter for a given source.

        If commands filter is defined for given source, returns default
        filter.

        :param item: Source to get commands filter for
        :type item: Path
        :return: Command filter for given source
        :rtype: CommandsFilter
        """
        for specified_source, commands_filter in self.sources_filters_map.items():
            try:
                item.relative_to(specified_source)
                return commands_filter
            except ValueError:
                continue
        return CommandsFilter()

    @property
    def sources_list(self) -> List[Path]:
        """Get list of all available sources."""
        return list(self.sources_filters_map.keys())

    def reset(self):
        """Reset sources repository."""
        self.sources_filters_map.clear()

    def update_from_config(
        self, config: MutableMapping[str, Any], contexts_repository: ContextsRepository
    ):
        """
        Update sources repository from configuration mapping.

        This is done using an existing contexts repository to link contexts
        from config to existing context objects


        :param config: Configuration to update repository from
        :type config: MutableMapping[str, Any]
        :param contexts_repository: Contexts repository to get context objects
            from
        :type contexts_repository: ContextsRepository

        """
        for source, commands_filter_config in config.items():
            contexts = [
                contexts_repository[context_name]
                for context_name in commands_filter_config.get(CONTEXTS, [])
            ]
            self.sources_filters_map[Path(source)] = CommandsFilter(
                contexts=contexts,
                allowed_commands=commands_filter_config.get(ALLOW_LIST, None),
                denied_commands=commands_filter_config.get(DENY_LIST, None),
            )
