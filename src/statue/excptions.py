"""Exceptions module."""


class StatueException(Exception):
    """Exceptions base for Statue."""


class UnknownCommand(StatueException):
    def __init__(self, command_name):
        super().__init__(f'Could not find command named "{command_name}".')


class InvalidCommand(StatueException):
    def __init__(self, command_name, contexts, allow_list, deny_list):
        super().__init__(
            f'The command "{command_name}" does not match the restrictions: '
            f"contexts={contexts}, allow_list={allow_list}, deny_list={deny_list}"
        )
