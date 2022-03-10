"""Commands map allow us to know which commands to run on each source."""
import itertools
from typing import Set


class CommandsMap(dict):
    """A mapping from source path to commands to run on it."""

    @property
    def total_commands_count(self) -> int:
        """How many commands total in the commands map."""
        return sum([len(value) for value in self.values()])

    @property
    def command_names(self) -> Set[str]:
        """All command names in map."""
        return set(
            itertools.chain.from_iterable(
                [command.name for command in sources_commands]
                for sources_commands in self.values()
            )
        )
