import itertools
import json

from pytest_cases import fixture

from statue.cli.cli import statue_cli
from statue.constants import SOURCES
from statue.exceptions import (
    CommandExecutionError,
    MissingConfiguration,
    UnknownContext,
)
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
from tests.util import command_mock


def build_commands_map():
    return {
        SOURCE1: [
            command_mock(name=COMMAND1, return_code=0),
            command_mock(name=COMMAND2, return_code=0),
        ],
        SOURCE2: [
            command_mock(name=COMMAND1, return_code=0),
            command_mock(name=COMMAND3, return_code=0),
            command_mock(name=COMMAND4, return_code=0),
        ],
    }


@fixture
def mock_read_commands_map(mocker):
    return mocker.patch("statue.cli.run.read_commands_map")


def assert_successful_run(result):
    assert result.exit_code == 0, f"Returned not zero with {result.exception}"
    assert "Statue finished successfully!" in result.output


def assert_usage_was_shown(result):
    assert result.exit_code == 0
    assert result.output.startswith("Usage: statue run [OPTIONS] [SOURCES]...")


def test_simple_run(
    cli_runner, mock_read_commands_map, mock_cache_save_evaluation, mock_cwd
):
    mock_read_commands_map.return_value = build_commands_map()

    result = cli_runner.invoke(statue_cli, ["run"])

    assert_successful_run(result)
    mock_read_commands_map.assert_called_once()
    mock_cache_save_evaluation.assert_called_once()


def test_run_with_no_cache(
    cli_runner, mock_read_commands_map, mock_cache_save_evaluation, mock_cwd
):
    mock_read_commands_map.return_value = build_commands_map()

    result = cli_runner.invoke(statue_cli, ["run", "--no-cache"])

    assert_successful_run(result)
    mock_read_commands_map.assert_called_once()
    mock_cache_save_evaluation.assert_not_called()


def test_run_and_install_uninstalled_commands(
    cli_runner, mock_read_commands_map, mock_cache_save_evaluation, mock_cwd
):
    command1 = command_mock(COMMAND1, installed=True, return_code=0)
    command2 = command_mock(COMMAND2, installed=False, return_code=0)
    command3 = command_mock(COMMAND3, installed=True, return_code=0)
    mock_read_commands_map.return_value = {
        SOURCE1: [command1, command2],
        SOURCE2: [command3]
    }

    result = cli_runner.invoke(statue_cli, ["run", "-i"])

    assert_successful_run(result)
    mock_read_commands_map.assert_called_once()
    mock_cache_save_evaluation.assert_called_once()

    command1.update_to_version.assert_not_called()
    command2.update_to_version.assert_called_once_with(verbosity=DEFAULT_VERBOSITY)
    command3.update_to_version.assert_not_called()


def test_run_and_save_to_file(
    cli_runner,
    mock_read_commands_map,
    mock_cache_save_evaluation,
    tmpdir_factory,
    mock_cwd,
):
    mock_read_commands_map.return_value = build_commands_map()
    output_path = tmpdir_factory.mktemp("bla") / "output.json"

    assert not output_path.exists()

    result = cli_runner.invoke(statue_cli, ["run", "-o", str(output_path)])

    assert_successful_run(result)
    mock_read_commands_map.assert_called_once()
    mock_cache_save_evaluation.assert_called_once()

    with open(output_path, mode="r", encoding="utf-8") as fd:
        saved_evaluation = json.load(fd)
    assert set(saved_evaluation.keys()) == set(build_commands_map().keys())


def test_run_over_recent_commands(
    cli_runner,
    mock_cache_evaluation_path,
    mock_evaluation_load_from_file,
    tmp_path_factory,
    mock_cwd,
):
    recent_cache = tmp_path_factory.mktemp("cache.json")
    mock_cache_evaluation_path.return_value = recent_cache
    mock_evaluation_load_from_file.return_value.commands_map = build_commands_map()

    result = cli_runner.invoke(statue_cli, ["run", "-r"])

    assert_successful_run(result)
    mock_cache_evaluation_path.assert_called_once_with(0)
    mock_evaluation_load_from_file.assert_called_once_with(recent_cache)


def test_run_over_failed_commands(
    cli_runner,
    mock_cache_evaluation_path,
    mock_evaluation_load_from_file,
    tmp_path_factory,
    mock_cwd,
):
    recent_cache = tmp_path_factory.mktemp("cache.json")
    mock_cache_evaluation_path.return_value = recent_cache
    mock_evaluation_load_from_file.return_value.failure_map = build_commands_map()

    result = cli_runner.invoke(statue_cli, ["run", "-f"])

    assert_successful_run(result)
    mock_cache_evaluation_path.assert_called_once_with(0)
    mock_evaluation_load_from_file.assert_called_once_with(recent_cache)


def test_run_over_previous_commands(
    cli_runner,
    mock_cache_evaluation_path,
    mock_evaluation_load_from_file,
    tmp_path_factory,
    mock_cwd,
):
    n = 5
    recent_cache = tmp_path_factory.mktemp("cache.json")
    mock_cache_evaluation_path.return_value = recent_cache
    mock_evaluation_load_from_file.return_value.commands_map = build_commands_map()

    result = cli_runner.invoke(statue_cli, ["run", "-p", n])

    assert_successful_run(result)
    mock_cache_evaluation_path.assert_called_once_with(n - 1)
    mock_evaluation_load_from_file.assert_called_once_with(recent_cache)


def test_run_over_previous_failed_commands(
    cli_runner,
    mock_cache_evaluation_path,
    mock_evaluation_load_from_file,
    tmp_path_factory,
    mock_cwd,
):
    n = 5
    recent_cache = tmp_path_factory.mktemp("cache.json")
    mock_cache_evaluation_path.return_value = recent_cache
    mock_evaluation_load_from_file.return_value.failure_map = build_commands_map()

    result = cli_runner.invoke(statue_cli, ["run", "-f", "-p", n])

    assert_successful_run(result)
    mock_cache_evaluation_path.assert_called_once_with(n - 1)
    mock_evaluation_load_from_file.assert_called_once_with(recent_cache)


def test_run_over_recent_commands_with_empty_cache(
    cli_runner,
    mock_cache_evaluation_path,
    mock_cwd,
):
    mock_cache_evaluation_path.return_value = None

    result = cli_runner.invoke(statue_cli, ["run", "-r"])

    assert_usage_was_shown(result)
    mock_cache_evaluation_path.assert_called_once_with(0)


def test_run_has_failed(
    cli_runner,
    mock_read_commands_map,
    mock_cache_save_evaluation,
    mock_cwd,
):
    commands_map = {
        SOURCE1: [
            command_mock(name=COMMAND1, return_code=0),
            command_mock(name=COMMAND2, return_code=1),
        ],
        SOURCE2: [
            command_mock(name=COMMAND1, return_code=0),
            command_mock(name=COMMAND3, return_code=1),
            command_mock(name=COMMAND4, return_code=0),
        ],
    }
    failure_map = {
        SOURCE1: [command_mock(name=COMMAND2, return_code=1)],
        SOURCE2: [command_mock(name=COMMAND3, return_code=1)],
    }
    mock_read_commands_map.return_value = commands_map

    result = cli_runner.invoke(statue_cli, ["run"])

    assert result.exit_code == 1
    mock_read_commands_map.assert_called_once()
    mock_cache_save_evaluation.assert_called_once()
    for source, commands in failure_map.items():
        failure_string = (
            f"{source}:\n" f"\t{', '.join([command.name for command in commands])}"
        )
        assert failure_string in result.output


def test_run_with_unknown_context(
    cli_runner,
    mock_read_commands_map,
    mock_cache_save_evaluation,
    mock_cwd,
):
    mock_read_commands_map.side_effect = UnknownContext(
        context_name=NOT_EXISTING_CONTEXT
    )

    result = cli_runner.invoke(statue_cli, ["run"])

    assert result.exit_code == 1
    assert f'Could not find context named "{NOT_EXISTING_CONTEXT}".' in result.output
    mock_cache_save_evaluation.assert_not_called()


def test_run_with_missing_configuration(
    cli_runner,
    mock_read_commands_map,
    mock_cache_save_evaluation,
    mock_cwd,
):
    mock_read_commands_map.side_effect = MissingConfiguration(part_name=SOURCES)

    result = cli_runner.invoke(statue_cli, ["run"])

    assert result.exit_code == 1
    assert (
        '"Run" command cannot be run without a specified source '
        "or a sources section in Statue's configuration.\n"
        'Please consider running "statue config init" in order to initialize '
        "default configuration."
    ) in result.output
    mock_cache_save_evaluation.assert_not_called()


def test_run_with_none_commands_map(
    cli_runner,
    mock_read_commands_map,
    mock_cache_save_evaluation,
    mock_cwd,
):
    mock_read_commands_map.return_value = None

    result = cli_runner.invoke(statue_cli, ["run"])
    assert_usage_was_shown(result)
    mock_cache_save_evaluation.assert_not_called()


def test_run_uninstalled_command(
    cli_runner, mock_read_commands_map, mock_cache_save_evaluation, mock_cwd
):
    command1 = command_mock(COMMAND1, installed=True, return_code=0)
    command2 = command_mock(COMMAND2, installed=False, return_code=0)
    command3 = command_mock(COMMAND3, installed=True, return_code=0)
    mock_read_commands_map.return_value = {
        SOURCE1: [command1, command2],
        SOURCE2: [command3]
    }

    result = cli_runner.invoke(statue_cli, ["run"])

    assert result.exit_code == 1
    assert (
       "The following commands are not installed correctly: command2\n"
       "Consider using the '-i' flag in order to install missing commands before running"
    ) in result.output
    mock_read_commands_map.assert_called_once()
    mock_cache_save_evaluation.assert_not_called()
