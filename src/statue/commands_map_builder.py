"""Designated class for building commands map."""
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

from statue.commands_filter import CommandsFilter
from statue.commands_map import CommandsMap
from statue.config.configuration import Configuration
from statue.context import Context
from statue.evaluation import Evaluation
from statue.exceptions import CacheError, CommandsMapBuilderError


@dataclass
class CommandsMapBuilder:  # pylint: disable=too-many-instance-attributes
    """Commands map builder class."""

    configuration: Configuration
    specified_sources: Optional[List[Path]] = None
    allowed_commands: Optional[List[str]] = None
    denied_commands: Optional[List[str]] = None
    contexts: List[Context] = field(default_factory=list)
    previous: Optional[int] = None
    failed: bool = False
    failed_only: bool = False

    @property
    def default_filter(self):
        """Get default filters for commands map."""
        return CommandsFilter(
            contexts=self.contexts,
            allowed_commands=self.allowed_commands,
            denied_commands=self.denied_commands,
        )

    @property
    def build_from_cache(self) -> bool:
        """Should build commands map using cached evaluations."""
        return self.previous is not None or self.failed or self.failed_only

    def build(self) -> CommandsMap:
        """
        Build commands map using the builders settings.

        :return: Commands map from instruction
        :rtype: CommandsMap
        :raises CommandsMapBuilderError: Raised when no sources where specified
        """
        if self.failed and self.previous is not None:
            raise CommandsMapBuilderError(
                '"failed" and "previous" cannot both be set when building commands map'
            )
        if not self.build_from_cache:
            sources = self.get_sources()
            if len(sources) == 0:
                raise CommandsMapBuilderError(
                    "No source was specified and no Sources section in configuration."
                )
            return self.configuration.build_commands_map(
                sources=sources, commands_filter=self.default_filter
            )
        evaluation = self.get_evaluation_from_cache()
        if self.failed_only:
            return evaluation.failure_evaluation.commands_map
        return evaluation.commands_map

    def get_evaluation_from_cache(self) -> Evaluation:
        """
        Get evaluation from cache based on flags.

        :return: Desired evaluation object
        :rtype: Evaluation
        :raises CommandsMapBuilderError: Raised when cannot get evaluation from cache.
        """
        try:
            if self.previous is not None:
                return self.configuration.cache.get_evaluation(self.previous - 1)
            return self.configuration.cache.recent_failed_evaluation
        except CacheError as error:
            raise CommandsMapBuilderError(str(error)) from error

    def get_sources(self) -> List[Path]:
        """
        Get sources list for the commands map.

        :return: Sources list for the commands map
        :rtype: List[Path]
        """
        if self.specified_sources is None or len(self.specified_sources) == 0:
            return self.configuration.sources_repository.sources_list
        return list(self.specified_sources)
