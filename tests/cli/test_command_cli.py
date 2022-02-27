from unittest import mock

from statue.cli import statue_cli
from statue.command import Command
from statue.command_builder import CommandBuilder
from statue.commands_filter import CommandsFilter
from statue.exceptions import UnknownCommand
from statue.verbosity import DEFAULT_VERBOSITY, VERBOSE
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


def test_commands_list(cli_runner, clear_configuration, mock_build_commands):
    mock_build_commands.return_value = [
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
    mock_build_commands.assert_called_once_with(CommandsFilter())


def test_commands_show_existing_command(
    cli_runner, clear_configuration, mock_get_command_builder
):
    mock_get_command_builder.return_value = CommandBuilder(
        COMMAND2, help=COMMAND_HELP_STRING2, default_args=[ARG3]
    )
    result = cli_runner.invoke(statue_cli, ["command", "show", COMMAND2])
    assert result.exit_code == 0, f"Existed with exception: {result.exception}"
    assert result.output == (
        f"Name - {COMMAND2}\n"
        f"Description - {COMMAND_HELP_STRING2}\n"
        f"Default arguments - ['{ARG3}']\n"
    ), "Show output is different than expected."


def test_commands_show_unknown_command_side_effect(
    cli_runner, clear_configuration, mock_get_command_builder
):
    mock_get_command_builder.side_effect = UnknownCommand(NOT_EXISTING_COMMAND)
    result = cli_runner.invoke(statue_cli, ["command", "show", NOT_EXISTING_COMMAND])
    assert result.exit_code == 1, "show command should exit with failure."
    assert (
        result.output == f'Could not find command named "{NOT_EXISTING_COMMAND}"\n'
    ), "Show output is different than expected."


def test_command_install_with_default_verbosity(
    cli_runner, clear_configuration, mock_build_commands
):
    commands = [mock.Mock(), mock.Mock(), mock.Mock()]
    mock_build_commands.return_value = commands
    result = cli_runner.invoke(statue_cli, ["command", "install"])
    for command in commands:
        command.install.assert_called_with(verbosity=DEFAULT_VERBOSITY)
    assert result.exit_code == 0, "Show command returned with no success code"


def test_command_install_with_verbose(
    cli_runner, clear_configuration, mock_build_commands
):
    commands = [mock.Mock(), mock.Mock(), mock.Mock()]
    mock_build_commands.return_value = commands
    result = cli_runner.invoke(statue_cli, ["command", "install", "--verbose"])
    for command in commands:
        command.install.assert_called_with(verbosity=VERBOSE)
    assert result.exit_code == 0, "Show command returned with no success code"
