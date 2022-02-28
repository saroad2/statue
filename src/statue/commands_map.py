"""Commands map allow us to know which commands to run on each source."""


class CommandsMap(dict):
    """A mapping from source path to commands to run on it."""

    @property
    def total_commands_count(self):
        """How many commands total in the commands map."""
        return sum([len(value) for value in self.values()])
