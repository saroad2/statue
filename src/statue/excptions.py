"""Exceptions module."""
from typing import List, Optional


class StatueException(Exception):
    """Exceptions base for Statue."""


class EmptyConfiguration(StatueException):
    """Configuration must be set."""

    def __init__(self) -> None:
        """Exception constructor."""
        super().__init__("Statue configuration is empty!")


class InvalidStatueConfiguration(StatueException):
    """User-Defined Statue configuration is invalid."""


class MissingConfiguration(InvalidStatueConfiguration):
    """Part of the Statue configuration is missing."""

    def __init__(self, part_name: str) -> None:
        """Exception constructor."""
        super().__init__(f'"{part_name}" is missing from Statue configuration.')


class UnknownCommand(StatueException):
    """Command isn't recognized."""

    def __init__(self, command_name: str) -> None:
        """Exception constructor."""
        super().__init__(f'Could not find command named "{command_name}".')


class InvalidCommand(StatueException):
    """Command doesn't fit restrictions."""

    def __init__(
        self,
        command_name: str,
        contexts: Optional[List[str]] = None,
        allow_list: Optional[List[str]] = None,
        deny_list: Optional[List[str]] = None,
    ) -> None:
        """Exception constructor."""
        super().__init__(
            f'The command "{command_name}" does not match the restrictions: '
            f"contexts={contexts}, allow_list={allow_list}, deny_list={deny_list}"
        )


class UnknownContext(StatueException):
    """Context isn't recognized."""

    def __init__(self, context_name: str) -> None:
        """Exception constructor."""
        super().__init__(f'Could not find context named "{context_name}".')
