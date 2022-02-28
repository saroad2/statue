"""Filter commands using simple checks."""
from typing import Any, Collection, FrozenSet, Optional

from statue.command_builder import CommandBuilder
from statue.context import Context


class CommandsFilter:
    """Filter data class for filtering command builders."""

    def __init__(
        self,
        contexts: Optional[Collection[Context]] = None,
        allowed_commands: Optional[Collection[str]] = None,
        denied_commands: Optional[Collection[str]] = None,
    ):
        """
        Initialize commands filter.

        :param contexts: Filter contexts
        :type contexts: Optional[Collection[Context]]
        :param allowed_commands: Allowed commands that pass filter
        :type allowed_commands: Optional[Collection[str]]
        :param denied_commands: Denied commands that does not pass filter
        :type denied_commands: Optional[Collection[str]]
        :raises ValueError: Raised if both allowed and denied commands are set.
        """
        self._contexts = frozenset() if contexts is None else frozenset(contexts)
        self._allowed_commands = (
            None if allowed_commands is None else frozenset(allowed_commands)
        )
        self._denied_commands = (
            None if denied_commands is None else frozenset(denied_commands)
        )
        if self.allowed_commands is not None and self.denied_commands is not None:
            raise ValueError(
                "Commands filter cannot be set with both allowed and denied commands"
            )

    @property
    def contexts(self):
        """Filter contexts."""
        return self._contexts

    @property
    def allowed_commands(self):
        """Filter allowed commands."""
        return self._allowed_commands

    @property
    def denied_commands(self):
        """Filter denied commands."""
        return self._denied_commands

    def __eq__(self, other: object) -> bool:
        """
        Compare command filters.

        :param other: Other object to compare to
        :type other: object
        :return: is equal
        :rtype: bool
        """
        return (
            isinstance(other, CommandsFilter)
            and self.contexts == other.contexts
            and self.allowed_commands == other.allowed_commands
            and self.denied_commands == other.denied_commands
        )

    def __str__(self) -> str:
        """
        Self as string.

        :return: Self as a representation string
        :rtype: str
        """
        return repr(self)

    def __repr__(self) -> str:
        """
        Representation string.

        :return: Self as a representation string
        :rtype: str
        """
        return (
            "CommandsFilter("
            f"contexts={self.contexts}, "
            f"allowed_commands={self.allowed_commands}, "
            f"denied_commands={self.denied_commands})"
        )

    def pass_filter(self, command_builder: CommandBuilder) -> bool:
        """
        Check if given command builder pass this filter.

        :param command_builder: Commands builder to be checked
        :type command_builder: CommandBuilder
        :return: Does this command builder pass the filter
        :rtype: bool
        """
        if (
            self.allowed_commands is not None
            and command_builder.name not in self.allowed_commands
        ):
            return False
        if (
            self.denied_commands is not None
            and command_builder.name in self.denied_commands
        ):
            return False
        return command_builder.match_contexts(*self.contexts)

    @classmethod
    def merge(
        cls, filter1: "CommandsFilter", filter2: "CommandsFilter"
    ) -> "CommandsFilter":
        """
        Merge two command filters into one filter.

        :param filter1: First filter to be merged
        :type filter1: CommandsFilter
        :param filter2: Second filter to be merged
        :type filter2: CommandsFilter
        :return: Merged filter
        :rtype: CommandsFilter
        :raises ValueError: Raised when a command is allowed in one filter
            and denied in another
        """
        contexts = filter1.contexts.union(filter2.contexts)
        allowed_commands = cls._intersect_optional_sets(
            filter1.allowed_commands, filter2.allowed_commands
        )
        denied_commands = cls._union_optional_sets(
            filter1.denied_commands, filter2.denied_commands
        )
        if allowed_commands is not None and denied_commands is not None:
            both_allowed_and_denied = allowed_commands.intersection(denied_commands)
            if len(both_allowed_and_denied) != 0:
                raise ValueError(
                    "Cannot merge command filters because the following commands "
                    "are both allowed and denied: "
                    f"{', '.join(both_allowed_and_denied)}"
                )
            denied_commands = None
        return CommandsFilter(
            contexts=frozenset(contexts),
            allowed_commands=allowed_commands,
            denied_commands=denied_commands,
        )

    @classmethod
    def _union_optional_sets(
        cls, set1: Optional[FrozenSet[Any]], set2: Optional[FrozenSet[Any]]
    ) -> Optional[FrozenSet[Any]]:
        if set1 is None and set2 is None:
            return None
        set1 = frozenset() if set1 is None else set1
        set2 = frozenset() if set2 is None else set2
        return set1.union(set2)

    @classmethod
    def _intersect_optional_sets(
        cls, set1: Optional[FrozenSet[Any]], set2: Optional[FrozenSet[Any]]
    ) -> Optional[FrozenSet[Any]]:
        if set1 is None:
            return set2
        if set2 is None:
            return set1
        return set1.intersection(set2)
