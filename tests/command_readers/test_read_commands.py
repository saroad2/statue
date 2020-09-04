from statue.command import Command
from statue.configuration import Configuration
from statue.excptions import InvalidCommand
from tests.constants import (
    ARG1,
    ARG2,
    ARG3,
    ARG4,
    ARG5,
    COMMAND1,
    COMMAND2,
    COMMAND3,
    COMMAND4,
    COMMAND5,
    COMMAND_HELP_STRING1,
    COMMAND_HELP_STRING2,
    COMMAND_HELP_STRING3,
    CONTEXT1,
    CONTEXT2,
    CONTEXT3,
)


def test_read_commands_success(mock_read_command, mock_commands_names_list):
    command1, command2, command3 = (
        Command(COMMAND1, help=COMMAND_HELP_STRING1),
        Command(COMMAND2, help=COMMAND_HELP_STRING2, args=[ARG1, ARG2]),
        Command(COMMAND3, help=COMMAND_HELP_STRING3, args=[ARG3, ARG4, ARG5]),
    )
    commands = [command1, command2, command3]
    mock_commands_names_list.return_value = [
        command1.name,
        command2.name,
        command3.name,
    ]
    mock_read_command.side_effect = [command1, command2, command3]
    kwargs = dict(contexts=[CONTEXT1], deny_list=[COMMAND4], allow_list=None)
    actual_commands = Configuration.read_commands(**kwargs)
    assert actual_commands == commands, "Commands are different than expected"
    mock_commands_names_list.assert_called_once_with()
    for returned_command in commands:
        mock_read_command.assert_any_call(command_name=returned_command.name, **kwargs)


def test_read_commands_failure(mock_read_command, mock_commands_names_list):
    command1, command3 = (
        Command(COMMAND1, help=COMMAND_HELP_STRING1),
        Command(COMMAND3, help=COMMAND_HELP_STRING3, args=[ARG3, ARG4, ARG5]),
    )
    commands = [command1, command3]
    mock_commands_names_list.return_value = [
        command1.name,
        COMMAND2,
        command3.name,
        COMMAND4,
        COMMAND5,
    ]

    def read_command_side_effect(command_name, **kwargs):
        command = {COMMAND1: command1, COMMAND3: command3}.get(command_name)
        if command is None:
            raise InvalidCommand(command_name)
        return command

    mock_read_command.side_effect = read_command_side_effect
    read_kwargs = dict(
        contexts=[CONTEXT2, CONTEXT3], deny_list=[COMMAND4], allow_list=None
    )
    actual_commands = Configuration.read_commands(**read_kwargs)
    assert actual_commands == commands, "Commands are different than expected"
    mock_commands_names_list.assert_called_once_with()
    for returned_command in commands:
        mock_read_command.assert_any_call(
            command_name=returned_command.name, **read_kwargs
        )
