"""Exceptions module."""
from typing import List, Optional


class StatueException(Exception):
    """Exceptions base for Statue."""


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
        contexts: Optional[List[str]],
        allow_list: Optional[List[str]],
        deny_list: Optional[List[str]],
    ) -> None:
        """Exception constructor."""
        super().__init__(
            f'The command "{command_name}" does not match the restrictions: '
            f"contexts={contexts}, allow_list={allow_list}, deny_list={deny_list}"
        )
