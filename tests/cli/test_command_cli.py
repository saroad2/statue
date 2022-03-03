from unittest import mock

from statue.cli import statue_cli
from statue.command_builder import CommandBuilder, ContextSpecification
from statue.verbosity import DEFAULT_VERBOSITY, VERBOSE
from tests.constants import (
    ARG1,
    ARG2,
    ARG3,
    ARG4,
    COMMAND1,
    COMMAND2,
    COMMAND3,
    COMMAND4,
    COMMAND_HELP_STRING1,
    COMMAND_HELP_STRING2,
    COMMAND_HELP_STRING3,
    COMMAND_HELP_STRING4,
    CONTEXT1,
    CONTEXT2,
    CONTEXT3,
    CONTEXT4,
    CONTEXT5,
    CONTEXT6,
    NOT_EXISTING_COMMAND,
)


def test_commands_list(cli_runner, mock_build_configuration_from_file):
    configuration = mock_build_configuration_from_file.return_value
    configuration.commands_repository.add_command_builders(
        CommandBuilder(COMMAND1, help=COMMAND_HELP_STRING1),
        CommandBuilder(COMMAND2, help=COMMAND_HELP_STRING2),
        CommandBuilder(COMMAND3, help=COMMAND_HELP_STRING3),
        CommandBuilder(COMMAND4, help=COMMAND_HELP_STRING4),
    )
    result = cli_runner.invoke(statue_cli, ["command", "list"])
    assert (
        result.exit_code == 0
    ), f"Exited unsuccessfully with the following exception: {result.exception}"
    assert result.output == (
        f"{COMMAND1} - {COMMAND_HELP_STRING1}\n"
        f"{COMMAND2} - {COMMAND_HELP_STRING2}\n"
        f"{COMMAND3} - {COMMAND_HELP_STRING3}\n"
        f"{COMMAND4} - {COMMAND_HELP_STRING4}\n"
    ), "List output is different than expected."


def test_commands_show_simple_command(cli_runner, mock_build_configuration_from_file):
    configuration = mock_build_configuration_from_file.return_value
    configuration.commands_repository.add_command_builders(
        CommandBuilder(COMMAND2, help=COMMAND_HELP_STRING2, default_args=[ARG3])
    )
    result = cli_runner.invoke(statue_cli, ["command", "show", COMMAND2])
    assert result.exit_code == 0, f"Exited with exception: {result.exception}"
    assert result.output == (
        f"Name - {COMMAND2}\n"
        f"Description - {COMMAND_HELP_STRING2}\n"
        f"Default arguments - {ARG3}\n"
    ), "Show output is different than expected."


def test_commands_show_command_with_required_contexts(
    cli_runner, mock_build_configuration_from_file
):
    configuration = mock_build_configuration_from_file.return_value
    configuration.commands_repository.add_command_builders(
        CommandBuilder(
            COMMAND2, help=COMMAND_HELP_STRING2, required_contexts=[CONTEXT1, CONTEXT2]
        )
    )
    result = cli_runner.invoke(statue_cli, ["command", "show", COMMAND2])
    assert result.exit_code == 0, f"Exited with exception: {result.exception}"
    assert result.output == (
        f"Name - {COMMAND2}\n"
        f"Description - {COMMAND_HELP_STRING2}\n"
        f"Required contexts - {CONTEXT1}, {CONTEXT2}\n"
    ), "Show output is different than expected."


def test_commands_show_command_with_allowed_contexts(
    cli_runner, mock_build_configuration_from_file
):
    configuration = mock_build_configuration_from_file.return_value
    configuration.commands_repository.add_command_builders(
        CommandBuilder(
            COMMAND2, help=COMMAND_HELP_STRING2, allowed_contexts=[CONTEXT1, CONTEXT2]
        )
    )
    result = cli_runner.invoke(statue_cli, ["command", "show", COMMAND2])
    assert result.exit_code == 0, f"Exited with exception: {result.exception}"
    assert result.output == (
        f"Name - {COMMAND2}\n"
        f"Description - {COMMAND_HELP_STRING2}\n"
        f"Allowed contexts - {CONTEXT1}, {CONTEXT2}\n"
    ), "Show output is different than expected."


def test_commands_show_command_with_specified_contexts(
    cli_runner, mock_build_configuration_from_file
):
    configuration = mock_build_configuration_from_file.return_value
    configuration.commands_repository.add_command_builders(
        CommandBuilder(
            COMMAND2,
            help=COMMAND_HELP_STRING2,
            contexts_specifications={
                CONTEXT1: ContextSpecification(args=[ARG1]),
                CONTEXT2: ContextSpecification(add_args=[ARG2]),
            },
        )
    )
    result = cli_runner.invoke(statue_cli, ["command", "show", COMMAND2])
    assert result.exit_code == 0, f"Exited with exception: {result.exception}"
    assert result.output == (
        f"Name - {COMMAND2}\n"
        f"Description - {COMMAND_HELP_STRING2}\n"
        f"Specified contexts - {CONTEXT1}, {CONTEXT2}\n"
    ), "Show output is different than expected."


def test_commands_show_command_with_multiple_contexts(
    cli_runner, mock_build_configuration_from_file
):
    configuration = mock_build_configuration_from_file.return_value
    configuration.commands_repository.add_command_builders(
        CommandBuilder(
            COMMAND2,
            help=COMMAND_HELP_STRING2,
            default_args=[ARG1, ARG2],
            required_contexts=[CONTEXT1, CONTEXT2],
            allowed_contexts=[CONTEXT3, CONTEXT4],
            contexts_specifications={
                CONTEXT5: ContextSpecification(args=[ARG3]),
                CONTEXT6: ContextSpecification(add_args=[ARG4]),
            },
        )
    )
    result = cli_runner.invoke(statue_cli, ["command", "show", COMMAND2])
    assert result.exit_code == 0, f"Exited with exception: {result.exception}"
    assert result.output == (
        f"Name - {COMMAND2}\n"
        f"Description - {COMMAND_HELP_STRING2}\n"
        f"Default arguments - {ARG1} {ARG2}\n"
        f"Required contexts - {CONTEXT1}, {CONTEXT2}\n"
        f"Allowed contexts - {CONTEXT3}, {CONTEXT4}\n"
        f"Specified contexts - {CONTEXT5}, {CONTEXT6}\n"
    ), "Show output is different than expected."


def test_commands_show_unknown_command_side_effect(
    cli_runner, mock_build_configuration_from_file
):
    result = cli_runner.invoke(statue_cli, ["command", "show", NOT_EXISTING_COMMAND])
    assert result.exit_code == 1, "show command should exit with failure."
    assert (
        result.output == f'Could not find command named "{NOT_EXISTING_COMMAND}"\n'
    ), "Show output is different than expected."


def test_command_install_with_default_verbosity(
    cli_runner, mock_build_configuration_from_file
):
    commands = [mock.Mock(), mock.Mock(), mock.Mock()]
    configuration = mock_build_configuration_from_file.return_value
    configuration.build_commands.return_value = commands
    result = cli_runner.invoke(statue_cli, ["command", "install"])
    for command in commands:
        command.install.assert_called_with(verbosity=DEFAULT_VERBOSITY)
    assert result.exit_code == 0, "Show command returned with no success code"


def test_command_install_with_verbose(cli_runner, mock_build_configuration_from_file):
    commands = [mock.Mock(), mock.Mock(), mock.Mock()]
    configuration = mock_build_configuration_from_file.return_value
    configuration.build_commands.return_value = commands
    result = cli_runner.invoke(statue_cli, ["command", "install", "--verbose"])
    for command in commands:
        command.install.assert_called_with(verbosity=VERBOSE)
    assert result.exit_code == 0, "Show command returned with no success code"
