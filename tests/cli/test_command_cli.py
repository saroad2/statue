from unittest.mock import Mock

import pytest

from statue.cli import statue as statue_cli
from statue.command import Command
from statue.verbosity import DEFAULT_VERBOSITY
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
    COMMAND_HELP_STRING1,
    COMMAND_HELP_STRING2,
    COMMAND_HELP_STRING3,
    COMMAND_HELP_STRING4,
    NOT_EXISTING_COMMAND,
)


@pytest.fixture
def mock_install_if_missing(monkeypatch):
    install_mock = Mock()
    monkeypatch.setattr("statue.cli.commands.install_commands_if_missing", install_mock)
    return install_mock


def test_commands_list(cli_runner, full_configuration):
    result = cli_runner.invoke(statue_cli, ["command", "list"])
    assert result.exit_code == 0, "list command should exit with success."
    assert result.output == (
        f"{COMMAND1} - {COMMAND_HELP_STRING1}\n"
        f"{COMMAND2} - {COMMAND_HELP_STRING2}\n"
        f"{COMMAND3} - {COMMAND_HELP_STRING3}\n"
        f"{COMMAND4} - {COMMAND_HELP_STRING4}\n"
    ), "List output is different than expected."


def test_commands_install(cli_runner, mock_install_if_missing, full_configuration):
    result = cli_runner.invoke(statue_cli, ["command", "install"])
    assert result.exit_code == 0, "install command should exit with success."
    assert result.output == "", "show output is different than expected."
    mock_install_if_missing.assert_called_with(
        [
            Command(name=COMMAND1, help=COMMAND_HELP_STRING1, args=[ARG1, ARG2],),
            Command(name=COMMAND2, help=COMMAND_HELP_STRING2, args=[ARG3],),
            Command(name=COMMAND3, help=COMMAND_HELP_STRING3, args=[]),
            Command(name=COMMAND4, help=COMMAND_HELP_STRING4, args=[ARG4, ARG5],),
        ],
        verbosity=DEFAULT_VERBOSITY,
    )


def test_commands_show_existing_command(cli_runner, full_configuration):
    result = cli_runner.invoke(statue_cli, ["command", "show", COMMAND2])
    assert result.exit_code == 0, "show command should exit with success."
    assert result.output == (
        f"Name - {COMMAND2}\n"
        f"Description - {COMMAND_HELP_STRING2}\n"
        f"Arguments - ['{ARG3}']\n"
    ), "Show output is different than expected."


def test_commands_show_non_existing_command(cli_runner, full_configuration):
    result = cli_runner.invoke(statue_cli, ["command", "show", NOT_EXISTING_COMMAND])
    assert result.exit_code == 1, "show command should exit with failure."
    assert (
        result.output == f'Could not find command named "{NOT_EXISTING_COMMAND}".\n'
    ), "Show output is different than expected."
