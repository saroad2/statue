from unittest import mock

import pytest

from statue.cli import statue as statue_cli
from statue.command import Command
from statue.excptions import InvalidCommand, UnknownCommand
from statue.verbosity import DEFAULT_VERBOSITY
from tests.constants import (
    ARG3,
    COMMAND1,
    COMMAND2,
    COMMAND3,
    COMMAND4,
    COMMAND_HELP_STRING1,
    COMMAND_HELP_STRING2,
    COMMAND_HELP_STRING3,
    COMMAND_HELP_STRING4,
    NOT_EXISTING_COMMAND,
)


@pytest.fixture
def mock_install_if_missing(monkeypatch):
    install_mock = mock.Mock()
    monkeypatch.setattr("statue.cli.commands.install_commands_if_missing", install_mock)
    return install_mock


def test_commands_list(cli_runner, mock_read_commands):
    mock_read_commands.return_value = [
        Command(COMMAND1, help=COMMAND_HELP_STRING1),
        Command(COMMAND2, help=COMMAND_HELP_STRING2),
        Command(COMMAND3, help=COMMAND_HELP_STRING3),
        Command(COMMAND4, help=COMMAND_HELP_STRING4),
    ]
    result = cli_runner.invoke(statue_cli, ["command", "list"])
    assert result.exit_code == 0, "list command should exit with success."
    assert result.output == (
        f"{COMMAND1} - {COMMAND_HELP_STRING1}\n"
        f"{COMMAND2} - {COMMAND_HELP_STRING2}\n"
        f"{COMMAND3} - {COMMAND_HELP_STRING3}\n"
        f"{COMMAND4} - {COMMAND_HELP_STRING4}\n"
    ), "List output is different than expected."
    mock_read_commands.assert_called_once_with(
        allow_list=tuple(), contexts=tuple(), deny_list=tuple()
    )


def test_commands_install(cli_runner, mock_install_if_missing, mock_read_commands):
    commands = [mock.Mock(), mock.Mock(), mock.Mock()]
    mock_read_commands.return_value = commands
    result = cli_runner.invoke(statue_cli, ["command", "install"])
    assert result.exit_code == 0, "install command should exit with success."
    assert result.output == "", "show output is different than expected."
    mock_install_if_missing.assert_called_with(commands, verbosity=DEFAULT_VERBOSITY)


def test_commands_show_existing_command(cli_runner, mock_read_command):
    mock_read_command.return_value = Command(
        COMMAND2, help=COMMAND_HELP_STRING2, args=[ARG3]
    )
    result = cli_runner.invoke(statue_cli, ["command", "show", COMMAND2])
    assert result.exit_code == 0, "show command should exit with success."
    assert result.output == (
        f"Name - {COMMAND2}\n"
        f"Description - {COMMAND_HELP_STRING2}\n"
        f"Arguments - ['{ARG3}']\n"
    ), "Show output is different than expected."


def test_commands_show_unknown_command_side_effect(cli_runner, mock_read_command):
    mock_read_command.side_effect = UnknownCommand(NOT_EXISTING_COMMAND)
    result = cli_runner.invoke(statue_cli, ["command", "show", NOT_EXISTING_COMMAND])
    assert result.exit_code == 1, "show command should exit with failure."
    assert (
        result.output == f'Could not find command named "{NOT_EXISTING_COMMAND}".\n'
    ), "Show output is different than expected."


def test_commands_show_invalid_command_side_effect(cli_runner, mock_read_command):
    mock_read_command.side_effect = InvalidCommand(NOT_EXISTING_COMMAND)
    result = cli_runner.invoke(statue_cli, ["command", "show", NOT_EXISTING_COMMAND])
    assert result.exit_code == 1, "show command should exit with failure."
    assert result.output == (
        f'The command "{NOT_EXISTING_COMMAND}" does not match the restrictions: '
        "contexts=None, allow_list=None, deny_list=None\n"
    ), "Show output is different than expected."
