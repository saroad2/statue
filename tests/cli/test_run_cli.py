from pathlib import Path

import mock
from pytest_cases import fixture

from statue.cli.cli import statue_cli
from statue.commands_filter import CommandsFilter
from statue.commands_map import CommandsMap
from statue.exceptions import UnknownContext
from statue.verbosity import DEFAULT_VERBOSITY
from tests.constants import (
    COMMAND1,
    COMMAND2,
    COMMAND3,
    COMMAND4,
    NOT_EXISTING_CONTEXT,
    SOURCE1,
    SOURCE2,
)
from tests.util import build_failure_evaluation, command_mock

EVALUATION_STRING = "This is an evaluation"


def build_commands_map():
    return CommandsMap(
        {
            SOURCE1: [
                command_mock(name=COMMAND1),
                command_mock(name=COMMAND2),
            ],
            SOURCE2: [
                command_mock(name=COMMAND1),
                command_mock(name=COMMAND3),
                command_mock(name=COMMAND4),
            ],
        }
    )


@fixture
def mock_evaluation_string(mocker):
    evaluation_string_mock = mocker.patch("statue.cli.run.evaluation_string")
    evaluation_string_mock.return_value = EVALUATION_STRING
    return evaluation_string_mock


def assert_evaluation_was_printed(result, evaluation_string_mock):
    evaluation_string_mock.assert_called_once()
    assert EVALUATION_STRING in result.output


def assert_usage_was_shown(result):
    assert result.exit_code == 0
    assert result.output.startswith("Usage: statue run [OPTIONS] [SOURCES]...")


def test_simple_run(
    cli_runner,
    mock_build_configuration_from_file,
    mock_cache_save_evaluation,
    mock_cwd,
    mock_evaluation_string,
):
    configuration = mock_build_configuration_from_file.return_value
    configuration.sources_repository[Path(SOURCE1)] = mock.Mock()
    configuration.sources_repository[Path(SOURCE2)] = mock.Mock()
    configuration.build_commands_map.return_value = build_commands_map()

    result = cli_runner.invoke(statue_cli, ["run"])

    assert (
        result.exit_code == 0
    ), f"Command failed with the following exception: {result.exception}"
    assert "Statue finished successfully" in result.output
    configuration.build_commands_map.assert_called_once_with(
        sources=[Path(SOURCE1), Path(SOURCE2)], commands_filter=CommandsFilter()
    )
    mock_cache_save_evaluation.assert_called_once()
    assert_evaluation_was_printed(result, mock_evaluation_string)


def test_run_with_no_cache(
    cli_runner,
    mock_build_configuration_from_file,
    mock_cache_save_evaluation,
    mock_cwd,
    mock_evaluation_string,
):
    configuration = mock_build_configuration_from_file.return_value
    configuration.sources_repository[Path(SOURCE1)] = mock.Mock()
    configuration.sources_repository[Path(SOURCE2)] = mock.Mock()
    configuration.build_commands_map.return_value = build_commands_map()

    result = cli_runner.invoke(statue_cli, ["run", "--no-cache"])

    assert (
        result.exit_code == 0
    ), f"Command failed with the following exception: {result.exception}"
    assert "Statue finished successfully" in result.output
    configuration.build_commands_map.assert_called_once()
    mock_cache_save_evaluation.assert_not_called()
    assert_evaluation_was_printed(result, mock_evaluation_string)


def test_run_and_install_uninstalled_commands(
    cli_runner,
    mock_build_configuration_from_file,
    mock_cache_save_evaluation,
    mock_cwd,
    mock_evaluation_string,
):
    command1 = command_mock(COMMAND1, installed=True)
    command2 = command_mock(COMMAND2, installed=False)
    command3 = command_mock(COMMAND3, installed=True)
    configuration = mock_build_configuration_from_file.return_value
    configuration.sources_repository[Path(SOURCE1)] = mock.Mock()
    configuration.sources_repository[Path(SOURCE2)] = mock.Mock()
    configuration.build_commands_map.return_value = CommandsMap(
        {
            SOURCE1: [command1, command2],
            SOURCE2: [command3],
        }
    )

    result = cli_runner.invoke(statue_cli, ["run", "-i"])

    assert (
        result.exit_code == 0
    ), f"Command failed with the following exception: {result.exception}"
    assert "Statue finished successfully" in result.output
    configuration.build_commands_map.assert_called_once()
    mock_cache_save_evaluation.assert_called_once()
    assert_evaluation_was_printed(result, mock_evaluation_string)

    command1.update_to_version.assert_not_called()
    command2.update_to_version.assert_called_once_with(verbosity=DEFAULT_VERBOSITY)
    command3.update_to_version.assert_not_called()


def test_run_and_save_to_file(
    cli_runner,
    mock_build_configuration_from_file,
    mock_cache_save_evaluation,
    mock_cwd,
    mock_evaluation_string,
    mock_evaluation_save_as_json,
):
    configuration = mock_build_configuration_from_file.return_value
    configuration.sources_repository[Path(SOURCE1)] = mock.Mock()
    configuration.sources_repository[Path(SOURCE2)] = mock.Mock()
    configuration.build_commands_map.return_value = build_commands_map()
    output_path = Path("path/to/output/dir")

    result = cli_runner.invoke(statue_cli, ["run", "-o", str(output_path)])

    assert (
        result.exit_code == 0
    ), f"Command failed with the following exception: {result.exception}"
    assert "Statue finished successfully" in result.output
    configuration.build_commands_map.assert_called_once()
    mock_cache_save_evaluation.assert_called_once()
    assert_evaluation_was_printed(result, mock_evaluation_string)

    mock_evaluation_save_as_json.assert_called_once_with(str(output_path))


def test_run_over_recent_commands(
    cli_runner,
    mock_build_configuration_from_file,
    mock_cache_evaluation_path,
    mock_evaluation_load_from_file,
    mock_cache_save_evaluation,
    tmp_path_factory,
    mock_cwd,
    mock_evaluation_string,
):
    recent_cache = tmp_path_factory.mktemp("cache.json")
    mock_cache_evaluation_path.return_value = recent_cache
    configuration = mock_build_configuration_from_file.return_value
    configuration.sources_repository[Path(SOURCE1)] = mock.Mock()
    configuration.sources_repository[Path(SOURCE2)] = mock.Mock()
    mock_evaluation_load_from_file.return_value.commands_map = build_commands_map()

    result = cli_runner.invoke(statue_cli, ["run", "-r"])

    assert (
        result.exit_code == 0
    ), f"Command failed with the following exception: {result.exception}"
    assert "Statue finished successfully" in result.output
    mock_cache_evaluation_path.assert_called_once_with(0)
    mock_evaluation_load_from_file.assert_called_once_with(recent_cache)
    mock_cache_save_evaluation.assert_called_once()
    assert_evaluation_was_printed(result, mock_evaluation_string)


def test_run_over_failed_commands(
    cli_runner,
    mock_build_configuration_from_file,
    mock_cache_evaluation_path,
    mock_cache_save_evaluation,
    mock_evaluation_load_from_file,
    tmp_path_factory,
    mock_cwd,
    mock_evaluation_string,
):
    recent_cache = tmp_path_factory.mktemp("cache.json")
    configuration = mock_build_configuration_from_file.return_value
    configuration.sources_repository[Path(SOURCE1)] = mock.Mock()
    configuration.sources_repository[Path(SOURCE2)] = mock.Mock()
    mock_cache_evaluation_path.return_value = recent_cache
    mock_evaluation_load_from_file.return_value.failure_evaluation = (
        build_failure_evaluation(build_commands_map())
    )

    result = cli_runner.invoke(statue_cli, ["run", "-f"])

    assert (
        result.exit_code == 0
    ), f"Command failed with the following exception: {result.exception}"
    assert "Statue finished successfully" in result.output
    mock_cache_evaluation_path.assert_called_once_with(0)
    mock_evaluation_load_from_file.assert_called_once_with(recent_cache)
    mock_cache_save_evaluation.assert_called_once()
    assert_evaluation_was_printed(result, mock_evaluation_string)


def test_run_over_previous_commands(
    cli_runner,
    mock_build_configuration_from_file,
    mock_cache_evaluation_path,
    mock_cache_save_evaluation,
    mock_evaluation_load_from_file,
    tmp_path_factory,
    mock_cwd,
    mock_evaluation_string,
):
    n = 5
    recent_cache = tmp_path_factory.mktemp("cache.json")
    configuration = mock_build_configuration_from_file.return_value
    configuration.sources_repository[Path(SOURCE1)] = mock.Mock()
    configuration.sources_repository[Path(SOURCE2)] = mock.Mock()
    mock_cache_evaluation_path.return_value = recent_cache
    mock_evaluation_load_from_file.return_value.commands_map = build_commands_map()

    result = cli_runner.invoke(statue_cli, ["run", "-p", n])

    assert (
        result.exit_code == 0
    ), f"Command failed with the following exception: {result.exception}"
    assert "Statue finished successfully" in result.output
    mock_cache_evaluation_path.assert_called_once_with(n - 1)
    mock_evaluation_load_from_file.assert_called_once_with(recent_cache)
    mock_cache_save_evaluation.assert_called_once()
    assert_evaluation_was_printed(result, mock_evaluation_string)


def test_run_over_previous_failed_commands(
    cli_runner,
    mock_build_configuration_from_file,
    mock_cache_evaluation_path,
    mock_cache_save_evaluation,
    mock_evaluation_load_from_file,
    tmp_path_factory,
    mock_cwd,
    mock_evaluation_string,
):
    n = 5
    recent_cache = tmp_path_factory.mktemp("cache.json")
    configuration = mock_build_configuration_from_file.return_value
    configuration.sources_repository[Path(SOURCE1)] = mock.Mock()
    configuration.sources_repository[Path(SOURCE2)] = mock.Mock()
    mock_cache_evaluation_path.return_value = recent_cache
    mock_evaluation_load_from_file.return_value.failure_evaluation = (
        build_failure_evaluation(build_commands_map())
    )

    result = cli_runner.invoke(statue_cli, ["run", "-f", "-p", n])

    assert (
        result.exit_code == 0
    ), f"Command failed with the following exception: {result.exception}"
    assert "Statue finished successfully" in result.output
    mock_cache_evaluation_path.assert_called_once_with(n - 1)
    mock_evaluation_load_from_file.assert_called_once_with(recent_cache)
    mock_cache_save_evaluation.assert_called_once()
    assert_evaluation_was_printed(result, mock_evaluation_string)


def test_run_over_recent_commands_with_empty_cache(
    cli_runner,
    mock_build_configuration_from_file,
    mock_cache_evaluation_path,
    mock_cwd,
    mock_evaluation_string,
):
    configuration = mock_build_configuration_from_file.return_value
    configuration.sources_repository[Path(SOURCE1)] = mock.Mock()
    configuration.sources_repository[Path(SOURCE2)] = mock.Mock()
    mock_cache_evaluation_path.return_value = None

    result = cli_runner.invoke(statue_cli, ["run", "-r"])

    assert_usage_was_shown(result)
    mock_cache_evaluation_path.assert_called_once_with(0)
    mock_evaluation_string.assert_not_called()


def test_run_has_failed(
    cli_runner,
    mock_build_configuration_from_file,
    mock_cache_save_evaluation,
    mock_cwd,
    mock_evaluation_string,
):
    commands_map = CommandsMap(
        {
            SOURCE1: [
                command_mock(name=COMMAND1),
                command_mock(name=COMMAND2, success=False),
            ],
            SOURCE2: [
                command_mock(name=COMMAND1),
                command_mock(name=COMMAND3, success=False),
                command_mock(name=COMMAND4),
            ],
        }
    )
    failure_evaluation = build_failure_evaluation(
        {
            SOURCE1: [command_mock(name=COMMAND2, success=False)],
            SOURCE2: [command_mock(name=COMMAND3, success=False)],
        }
    )
    configuration = mock_build_configuration_from_file.return_value
    configuration.sources_repository[Path(SOURCE1)] = mock.Mock()
    configuration.sources_repository[Path(SOURCE2)] = mock.Mock()
    configuration.build_commands_map.return_value = commands_map

    result = cli_runner.invoke(statue_cli, ["run"])

    assert result.exit_code == 1
    configuration.build_commands_map.assert_called_once()
    mock_cache_save_evaluation.assert_called_once()
    assert_evaluation_was_printed(result, mock_evaluation_string)

    for source, source_evaluation in failure_evaluation.items():
        failed_commands_string = ", ".join(
            [
                command_evaluation.command.name
                for command_evaluation in source_evaluation
            ]
        )
        failure_string = f"{source}:\n" f"\t{failed_commands_string}"
        assert failure_string in result.output


def test_run_with_unknown_context(
    cli_runner,
    mock_build_configuration_from_file,
    mock_cache_save_evaluation,
    mock_cwd,
    mock_evaluation_string,
):
    configuration = mock_build_configuration_from_file.return_value
    configuration.sources_repository[Path(SOURCE1)] = mock.Mock()
    configuration.sources_repository[Path(SOURCE2)] = mock.Mock()
    configuration.build_commands_map.side_effect = UnknownContext(
        context_name=NOT_EXISTING_CONTEXT
    )

    result = cli_runner.invoke(statue_cli, ["run"])

    assert result.exit_code == 1
    assert f'Could not find context named "{NOT_EXISTING_CONTEXT}"' in result.output
    mock_cache_save_evaluation.assert_not_called()
    mock_evaluation_string.assert_not_called()


def test_run_with_missing_configuration(
    cli_runner,
    mock_build_configuration_from_file,
    mock_cache_save_evaluation,
    mock_cwd,
    mock_evaluation_string,
):
    result = cli_runner.invoke(statue_cli, ["run"])

    assert result.exit_code == 1
    assert (
        '"Run" command cannot be run without a specified source '
        "or a sources section in Statue's configuration.\n"
        'Please consider running "statue config init" in order to initialize '
        "default configuration."
    ) in result.output
    mock_cache_save_evaluation.assert_not_called()
    mock_evaluation_string.assert_not_called()


def test_run_with_none_commands_map(
    cli_runner,
    mock_build_configuration_from_file,
    mock_cache_save_evaluation,
    mock_cwd,
    mock_evaluation_string,
):
    configuration = mock_build_configuration_from_file.return_value
    configuration.sources_repository[Path(SOURCE1)] = mock.Mock()
    configuration.sources_repository[Path(SOURCE2)] = mock.Mock()
    configuration.build_commands_map.return_value = None

    result = cli_runner.invoke(statue_cli, ["run"])
    assert_usage_was_shown(result)
    mock_cache_save_evaluation.assert_not_called()
    mock_evaluation_string.assert_not_called()


def test_run_uninstalled_command(
    cli_runner,
    mock_build_configuration_from_file,
    mock_cache_save_evaluation,
    mock_cwd,
    mock_evaluation_string,
):
    command1 = command_mock(COMMAND1, installed=True)
    command2 = command_mock(COMMAND2, installed=False)
    command3 = command_mock(COMMAND3, installed=True)
    configuration = mock_build_configuration_from_file.return_value
    configuration.sources_repository[Path(SOURCE1)] = mock.Mock()
    configuration.sources_repository[Path(SOURCE2)] = mock.Mock()
    configuration.build_commands_map.return_value = {
        SOURCE1: [command1, command2],
        SOURCE2: [command3],
    }

    result = cli_runner.invoke(statue_cli, ["run"])

    assert result.exit_code == 1
    assert (
        "The following commands are not installed correctly: command2\n"
        "Consider using the '-i' flag in order to install missing "
        "commands before running"
    ) in result.output
    configuration.build_commands_map.assert_called_once()
    mock_cache_save_evaluation.assert_not_called()
    mock_evaluation_string.assert_not_called()


def test_run_on_given_source(
    cli_runner,
    mock_build_configuration_from_file,
    mock_cache_save_evaluation,
    mock_cwd,
    mock_evaluation_string,
):
    configuration = mock_build_configuration_from_file.return_value
    configuration.build_commands_map.return_value = build_commands_map()

    result = cli_runner.invoke(statue_cli, ["run", SOURCE1])

    assert (
        result.exit_code == 0
    ), f"Command failed with the following exception: {result.exception}"
    assert "Statue finished successfully" in result.output
    configuration.build_commands_map.assert_called_once_with(
        sources=[Path(SOURCE1)], commands_filter=CommandsFilter()
    )
    mock_cache_save_evaluation.assert_called_once()
    assert_evaluation_was_printed(result, mock_evaluation_string)
