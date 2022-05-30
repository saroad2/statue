"""Place for saving all available sources with default commands filter."""
from collections import OrderedDict
from pathlib import Path
from typing import Any, Dict, List, Optional
from typing import OrderedDict as OrderedDictType

from statue.commands_filter import CommandsFilter
from statue.config.contexts_repository import ContextsRepository
from statue.constants import ALLOW_LIST, CONTEXTS, DENY_LIST
from statue.io_util import is_equal_or_child_of


class SourcesRepository:
    """
    Repository class for saving and accessing sources.

    This is done in order to get specific commands filter from each source.
    """

    def __init__(
        self, sources_filters_map: Optional[Dict[Path, CommandsFilter]] = None
    ):
        """
        Initialize repository.

        :param sources_filters_map: Map from a path to its commands filter
        :type sources_filters_map: Optional[Dict[Path, CommandsFilter]]
        """
        self.sources_filters_map: Dict[Path, CommandsFilter] = (
            {} if sources_filters_map is None else sources_filters_map
        )

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
            if is_equal_or_child_of(item, specified_source):
                return commands_filter
        return CommandsFilter()

    @property
    def sources_list(self) -> List[Path]:
        """Get list of all available sources."""
        return list(self.sources_filters_map.keys())

    def track_sources(self, *sources: Path):
        """
        Track sources with default commands filter.

        :param sources: Sources to track
        :type sources: Path
        """
        for source in sources:
            self[source] = CommandsFilter()

    def remove_source(self, source: Path):
        """
        Remove source from repository.

        :param source: Source to be removed
        :type source Path
        """
        del self.sources_filters_map[source]

    def reset(self):
        """Reset sources repository."""
        self.sources_filters_map.clear()

    def as_dict(self) -> OrderedDictType[str, Any]:
        """
        Encode sources repository as a dictionary.

        This is used in order to serialize the sources repository in
        a configuration file.

        :return: Serialized representation dictionary
        :rtype: Dict[str, Any]
        """
        sources_list = self.sources_list
        sources_list.sort(key=lambda source: source.as_posix())
        return OrderedDict(
            [(source.as_posix(), self[source].as_dict()) for source in sources_list]
        )

    @classmethod
    def from_dict(cls, config: Dict[str, Any], contexts_repository: ContextsRepository):
        """
        Create sources repository from configuration mapping.

        This is done using an existing contexts repository to link contexts
        from config to existing context objects


        :param config: Configuration to create repository from
        :type config: Dict[str, Any]
        :param contexts_repository: Contexts repository to get context objects
            from
        :type contexts_repository: ContextsRepository
        :return: Built sources repository
        :rtype: SourcesRepository
        """
        sources_filters_map = {}
        for source, commands_filter_config in config.items():
            contexts = [
                contexts_repository[context_name]
                for context_name in commands_filter_config.get(CONTEXTS, [])
            ]
            sources_filters_map[Path(source)] = CommandsFilter(
                contexts=contexts,
                allowed_commands=commands_filter_config.get(ALLOW_LIST, None),
                denied_commands=commands_filter_config.get(DENY_LIST, None),
            )
        return SourcesRepository(sources_filters_map)
