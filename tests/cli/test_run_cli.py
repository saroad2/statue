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

COMMANDS_MAP = {
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


def test_simple_run(
    cli_runner, mock_read_commands_map, mock_cache_save_evaluation, mock_cwd
):
    mock_read_commands_map.return_value = COMMANDS_MAP

    result = cli_runner.invoke(statue_cli, ["run"])

    assert_successful_run(result)
    mock_read_commands_map.assert_called_once()
    mock_cache_save_evaluation.assert_called_once()


def test_run_with_no_cache(
    cli_runner, mock_read_commands_map, mock_cache_save_evaluation, mock_cwd
):
    mock_read_commands_map.return_value = COMMANDS_MAP

    result = cli_runner.invoke(statue_cli, ["run", "--no-cache"])

    assert_successful_run(result)
    mock_read_commands_map.assert_called_once()
    mock_cache_save_evaluation.assert_not_called()


def test_run_and_install(
    cli_runner, mock_read_commands_map, mock_cache_save_evaluation, mock_cwd
):
    mock_read_commands_map.return_value = COMMANDS_MAP

    result = cli_runner.invoke(statue_cli, ["run", "-i"])

    assert_successful_run(result)
    mock_read_commands_map.assert_called_once()
    mock_cache_save_evaluation.assert_called_once()

    for command in itertools.chain.from_iterable(COMMANDS_MAP.values()):
        command.install.assert_called_once_with(verbosity=DEFAULT_VERBOSITY)


def test_run_and_save_to_file(
    cli_runner,
    mock_read_commands_map,
    mock_cache_save_evaluation,
    tmpdir_factory,
    mock_cwd,
):
    mock_read_commands_map.return_value = COMMANDS_MAP
    output_path = tmpdir_factory.mktemp("bla") / "output.json"

    assert not output_path.exists()

    result = cli_runner.invoke(statue_cli, ["run", "-o", str(output_path)])

    assert_successful_run(result)
    mock_read_commands_map.assert_called_once()
    mock_cache_save_evaluation.assert_called_once()

    with open(output_path, mode="r") as fd:
        saved_evaluation = json.load(fd)
    assert set(saved_evaluation.keys()) == set(COMMANDS_MAP.keys())


def test_run_over_failed_commands(
    cli_runner,
    mock_cache_recent_evaluation_path,
    mock_evaluation_load_from_file,
    tmp_path_factory,
    mock_cwd,
):
    recent_cache = tmp_path_factory.mktemp("cache.json")
    mock_cache_recent_evaluation_path.return_value = recent_cache
    mock_evaluation_load_from_file.return_value.failure_map = COMMANDS_MAP

    result = cli_runner.invoke(statue_cli, ["run", "-f"])

    assert_successful_run(result)
    mock_evaluation_load_from_file.assert_called_once_with(recent_cache)


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
    assert result.exit_code == 0
    assert result.output.startswith("Usage: statue run [OPTIONS] [SOURCES]...")
    mock_cache_save_evaluation.assert_not_called()


def test_run_with_command_raises_exception(
    cli_runner, mock_read_commands_map, mock_cache_save_evaluation, mock_cwd
):
    mock_read_commands_map.return_value = COMMANDS_MAP
    some_command = COMMANDS_MAP[SOURCE2][0]
    some_command.execute.side_effect = CommandExecutionError(
        command_name=some_command.name
    )

    result = cli_runner.invoke(statue_cli, ["run"])

    assert result.exit_code == 1
    assert 'Try to rerun with the "-i" flag' in result.output
    mock_read_commands_map.assert_called_once()
    mock_cache_save_evaluation.assert_not_called()
