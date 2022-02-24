"""Exceptions module."""


class StatueException(Exception):
    """Exceptions base for Statue."""


class StatueConfigurationError(StatueException):
    """User-Defined Statue configuration is invalid."""


class EmptyConfiguration(StatueConfigurationError):
    """Configuration must be set."""

    def __init__(self) -> None:
        """Exception constructor."""
        super().__init__("Statue configuration is empty!")


class MissingConfiguration(StatueConfigurationError):
    """Part of the Statue configuration is missing."""

    def __init__(self, part_name: str) -> None:
        """
        Exception constructor.

        :param part_name: The missing part from the configuration
        :type part_name: str
        """
        super().__init__(f'"{part_name}" is missing from Statue configuration.')


class InconsistentConfiguration(StatueConfigurationError):
    """Some of statue's configurations are inconsistent."""


class UnknownCommand(StatueException):
    """Command isn't recognized."""

    def __init__(self, command_name: str) -> None:
        """
        Exception constructor.

        :param command_name: Name of the unfound command
        :type command_name: str
        """
        super().__init__(f'Could not find command named "{command_name}".')


class InvalidCommand(StatueException):
    """Command doesn't fit restrictions."""


class UnknownContext(StatueException):
    """Context isn't recognized."""

    def __init__(self, context_name: str) -> None:
        """
        Exception constructor.

        :param context_name: Name of the unfound context
        :type context_name: str
        """
        super().__init__(f'Could not find context named "{context_name}"')


class CommandExecutionError(StatueException):
    """Command cannot be executed."""

    def __init__(self, command_name: str) -> None:
        """
        Exception constructor.

        :param command_name: Command name
        :type command_name: str
        """
        super().__init__(
            f'Cannot execute "{command_name}" because it is not installed.'
        )
