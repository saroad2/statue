from unittest.mock import Mock

import pytest

from statue.cli import statue as statue_cli
from tests.constants import COMMAND1, NOT_EXISTING_CONTEXT, SOURCE1

SIMPLE_RUN_OUTPUT = (
    "Evaluation\n"
    "==========\n"
    "\n"
    "Evaluating source1\n"
    "Command1\n"
    "--------\n"
    "Command2\n"
    "--------\n"
    "Command3\n"
    "--------\n"
    "Command4\n"
    "--------\n"
    "\n"
    "Evaluating source2\n"
    "Command1\n"
    "--------\n"
    "\n"
    "Evaluating source3\n"
    "Command1\n"
    "--------\n"
    "Command2\n"
    "--------\n"
    "\n"
    "Evaluating source4\n"
    "Command1\n"
    "--------\n"
    "Command2\n"
    "--------\n"
    "Command3\n"
    "--------\n"
    "Command4\n"
    "--------\n"
    "\n"
    "Evaluating source5\n"
    "Command1\n"
    "--------\n"
    "Command2\n"
    "--------\n"
    "Command3\n"
    "--------\n"
    "Command4\n"
    "--------\n"
    "\n"
    "Summary\n"
    "=======\n"
    "Statue finished successfully!\n"
)


@pytest.fixture
def mock_install_if_missing(monkeypatch):
    install_mock = Mock()
    monkeypatch.setattr("statue.cli.run.install_commands_if_missing", install_mock)
    return install_mock


def test_simple_run(
    cli_runner, full_configuration, mock_command_execute, mock_install_if_missing
):
    mock_command_execute.return_value = 0
    result = cli_runner.invoke(statue_cli, ["run"])
    assert result.exit_code == 0, "run command should exit with success."
    assert (
        result.output == SIMPLE_RUN_OUTPUT
    ), "run command output is different than expected."
    mock_install_if_missing.assert_not_called()


def test_run_and_install(
    cli_runner, full_configuration, mock_command_execute, mock_install_if_missing
):
    mock_command_execute.return_value = 0
    result = cli_runner.invoke(statue_cli, ["run", "-i"])
    assert result.exit_code == 0, "run command should exit with success."
    assert (
        result.output == SIMPLE_RUN_OUTPUT
    ), "run command output is different than expected."
    mock_install_if_missing.assert_called()


def test_run_silently(cli_runner, full_configuration, mock_command_execute):
    mock_command_execute.return_value = 0
    result = cli_runner.invoke(statue_cli, ["run", "--silent"])
    assert result.exit_code == 0, "run command should exit with success."
    assert result.output == (
        "Evaluation\n"
        "=========="
        "\n"
        "\n"
        "Summary\n"
        "======="
        "\n"
        "Statue finished successfully!\n"
    ), "run command output is different than expected."


def test_run_without_commands(cli_runner, empty_configuration, mock_command_execute):
    mock_command_execute.return_value = 0
    result = cli_runner.invoke(statue_cli, ["run"])
    assert result.exit_code == 0, "run command should exit with success."
    assert result.output == (
        "Usage: statue run [OPTIONS] [SOURCES]...\n"
        "\n"
        "  Run static code analysis commands on sources.\n"
        "\n"
        "  Source files to run Statue on can be presented as positional arguments. "
        "When\n"
        "  no source files are presented, will use configuration file to determine "
        "on\n"
        "  which files to run\n"
        "\n"
        "Options:\n"
        "  -c, --context TEXT              Context in which to evaluate the "
        "commands.\n"
        "  -a, --allow TEXT                Allowed command.\n"
        "  -d, --deny TEXT                 Denied command.\n"
        "  -i, --install                   Install commands before running if "
        "missing\n"
        '  --silent                        Set verbosity to "silent".\n'
        '  --verbose                       Set verbosity to "verbose".\n'
        "  --verbosity [normal|silent|verbose]\n"
        "                                  [default: normal]\n"
        "  --help                          Show this message and exit.\n"
    ), "run command output is different than expected."


def test_command_failure(cli_runner, full_configuration, mock_command_execute):
    mock_command_execute.side_effect = lambda args, verbosity: {
        (COMMAND1, SOURCE1): 1
    }.get((args[0], args[1]), 0)
    result = cli_runner.invoke(statue_cli, ["run"])
    assert result.exit_code == 1, "run command should exit with success."
    assert result.output == (
        "Evaluation\n"
        "==========\n"
        "\n"
        "Evaluating source1\n"
        "Command1\n"
        "--------\n"
        "Command2\n"
        "--------\n"
        "Command3\n"
        "--------\n"
        "Command4\n"
        "--------\n"
        "\n"
        "Evaluating source2\n"
        "Command1\n"
        "--------\n"
        "\n"
        "Evaluating source3\n"
        "Command1\n"
        "--------\n"
        "Command2\n"
        "--------\n"
        "\n"
        "Evaluating source4\n"
        "Command1\n"
        "--------\n"
        "Command2\n"
        "--------\n"
        "Command3\n"
        "--------\n"
        "Command4\n"
        "--------\n"
        "\n"
        "Evaluating source5\n"
        "Command1\n"
        "--------\n"
        "Command2\n"
        "--------\n"
        "Command3\n"
        "--------\n"
        "Command4\n"
        "--------\n"
        "\n"
        "Summary\n"
        "=======\n"
        "Statue has failed on the following commands:\n"
        "\n"
        "source1:\n"
        "\tcommand1\n"
    ), "run command output is different than expected."


def test_run_with_unknown_context(
    cli_runner, full_configuration, mock_command_execute, mock_install_if_missing
):
    mock_command_execute.return_value = 0
    result = cli_runner.invoke(statue_cli, ["run", "-c", NOT_EXISTING_CONTEXT])
    assert result.exit_code == 1, "run command should exit with failure."
    assert (
        result.output == f'Could not find context named "{NOT_EXISTING_CONTEXT}".\n'
    ), "run command output is different than expected."
    mock_install_if_missing.assert_not_called()
