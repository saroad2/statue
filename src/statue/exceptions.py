"""Exceptions module."""


class StatueException(Exception):
    """Exceptions base for Statue."""


# Configuration related exceptions


class StatueConfigurationError(StatueException):
    """User-Defined Statue configuration is invalid."""


class MissingConfiguration(StatueConfigurationError):
    """Part of the Statue configuration is missing."""

    message = "Statue was unable to load configuration"

    def __init__(self):
        """Exception constructor."""
        super().__init__(self.message)


class InvalidConfiguration(StatueConfigurationError):
    """Some of statue's configurations are invalid."""


class InconsistentConfiguration(StatueConfigurationError):
    """Some of statue's configurations are inconsistent."""


# Command related exceptions


class UnknownCommand(StatueException):
    """Command isn't recognized."""

    def __init__(self, command_name: str) -> None:
        """
        Exception constructor.

        :param command_name: Name of the unfound command
        :type command_name: str
        """
        super().__init__(f'Could not find command named "{command_name}"')


class InvalidCommand(StatueException):
    """Command doesn't fit restrictions."""


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


# Context related exceptions


class UnknownContext(StatueException):
    """Context isn't recognized."""

    def __init__(self, context_name: str) -> None:
        """
        Exception constructor.

        :param context_name: Name of the unfound context
        :type context_name: str
        """
        super().__init__(f'Could not find context named "{context_name}"')


class ContextCircularParentingError(StatueException):
    """Parent cannot be a child of its child."""

    def __init__(self, context1: str, context2: str):
        """
        Exception constructor.

        :param context1: Name of first context
        :type context1: str
        :param context2: Name of second context
        :type context2: str
        """
        super().__init__(
            "Cannot set circular parenting between " f'"{context1}" and "{context2}"'
        )


# Template related exceptions


class UnknownTemplate(StatueException):
    """Template isn't recognized."""

    def __init__(self, template_name: str) -> None:
        """
        Exception constructor.

        :param template_name: Name of the unfound template
        :type template_name: str
        """
        super().__init__(f'Could not find template named "{template_name}"')


# Cache related exceptions


class CacheError(StatueException):
    """Cache related exception."""
