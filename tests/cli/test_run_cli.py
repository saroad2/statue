import mock
import pytest

from statue.cli import statue_cli
from statue.exceptions import CommandsMapBuilderError, UnknownContext
from statue.runner import RunnerMode
from statue.verbosity import NORMAL, VERBOSE
from tests.constants import COMMAND1, COMMAND2, COMMAND3, CONTEXT1, SOURCE1
from tests.util import (
    command_builder_mock,
    failed_evaluation_mock,
    successful_evaluation_mock,
)

DEFAULT_EVALUATION_STRING = (
    "##############\n"
    "# Evaluation #\n"
    "##############\n"
    "This is a pretty evaluation string\n"
    "\n"
    "###########\n"
    "# Summary #\n"
    "###########\n"
    "\n"
    "This is a pretty evaluation summary string\n"
)


def run_flags(configuration, **kwargs):
    default_flags = dict(
        specified_sources=None,
        configuration=configuration,
        allowed_commands=None,
        denied_commands=None,
        contexts=[],
        previous=None,
        failed=False,
        failed_only=False,
    )
    default_flags.update(kwargs)
    return default_flags


@pytest.fixture
def mock_commands_map_builder(mocker):
    return mocker.patch("statue.cli.run.CommandsMapBuilder")


@pytest.fixture
def mock_build_runner(mocker):
    return mocker.patch("statue.cli.run.build_runner")


@pytest.fixture
def mock_evaluation_string(mocker):
    evaluation_string = mocker.patch("statue.cli.run.evaluation_string")
    evaluation_string.return_value = "This is a pretty evaluation string"
    return evaluation_string


@pytest.fixture
def mock_evaluation_summary_string(mocker):
    evaluation_summary_string = mocker.patch("statue.cli.run.evaluation_summary_string")
    evaluation_summary_string.return_value = (
        "This is a pretty evaluation summary string"
    )
    return evaluation_summary_string


# Successful runs


def test_run_cli_with_default_flags(
    cli_runner,
    mock_build_configuration_from_file,
    mock_commands_map_builder,
    mock_build_runner,
    mock_evaluation_string,
    mock_evaluation_summary_string,
):
    commands_builders = [
        command_builder_mock(COMMAND1),
        command_builder_mock(COMMAND2),
        command_builder_mock(COMMAND3),
    ]
    configuration = mock_build_configuration_from_file.return_value
    configuration.commands_repository = commands_builders
    commands_map = mock.MagicMock()
    commands_map.__len__.return_value = 3
    commands_map.command_names = [COMMAND1, COMMAND2, COMMAND3]
    mock_commands_map_builder.return_value.build.return_value = commands_map
    evaluation = successful_evaluation_mock()
    mock_build_runner.return_value.evaluate.return_value = evaluation

    result = cli_runner.invoke(statue_cli, ["run"])

    assert result.exit_code == 0, f"Failed with exception: {result.exception}"
    assert result.output == DEFAULT_EVALUATION_STRING
    mock_commands_map_builder.assert_called_once_with(**run_flags(configuration))
    mock_commands_map_builder.return_value.build.assert_called_once_with()
    mock_build_runner.assert_called_once_with("SYNC")
    mock_build_runner.return_value.evaluate.assert_called_once_with(commands_map)
    configuration.cache.save_evaluation.assert_called_once_with(evaluation)
    evaluation.save_as_json.assert_not_called()
    mock_evaluation_string.assert_called_once_with(evaluation, verbosity=NORMAL)


def test_run_cli_with_source(
    tmp_path,
    cli_runner,
    mock_build_configuration_from_file,
    mock_commands_map_builder,
    mock_build_runner,
    mock_evaluation_string,
    mock_evaluation_summary_string,
):
    source = tmp_path / SOURCE1
    source.touch()
    commands_builders = [
        command_builder_mock(COMMAND1),
        command_builder_mock(COMMAND2),
        command_builder_mock(COMMAND3),
    ]
    configuration = mock_build_configuration_from_file.return_value
    configuration.commands_repository = commands_builders
    commands_map = mock.MagicMock()
    commands_map.__len__.return_value = 3
    commands_map.command_names = [COMMAND1, COMMAND2, COMMAND3]
    mock_commands_map_builder.return_value.build.return_value = commands_map
    evaluation = successful_evaluation_mock()
    mock_build_runner.return_value.evaluate.return_value = evaluation

    result = cli_runner.invoke(statue_cli, ["run", str(source)])

    assert result.exit_code == 0, f"Failed with exception: {result.exception}"
    assert result.output == DEFAULT_EVALUATION_STRING
    mock_commands_map_builder.assert_called_once_with(
        **run_flags(configuration, specified_sources=[source])
    )
    mock_commands_map_builder.return_value.build.assert_called_once_with()
    mock_build_runner.assert_called_once_with("SYNC")
    mock_build_runner.return_value.evaluate.assert_called_once_with(commands_map)
    configuration.cache.save_evaluation.assert_called_once_with(evaluation)
    evaluation.save_as_json.assert_not_called()
    mock_evaluation_string.assert_called_once_with(evaluation, verbosity=NORMAL)


@pytest.mark.parametrize("context_flag", ["-c", "--context"])
def test_run_cli_with_context(
    context_flag,
    cli_runner,
    mock_build_configuration_from_file,
    mock_commands_map_builder,
    mock_build_runner,
    mock_evaluation_string,
    mock_evaluation_summary_string,
):
    commands_builders = [
        command_builder_mock(COMMAND1),
        command_builder_mock(COMMAND2),
        command_builder_mock(COMMAND3),
    ]
    context = mock.Mock()
    configuration = mock_build_configuration_from_file.return_value
    configuration.commands_repository = commands_builders
    configuration.contexts_repository = {CONTEXT1: context}
    commands_map = mock.MagicMock()
    commands_map.__len__.return_value = 3
    commands_map.command_names = [COMMAND1, COMMAND2, COMMAND3]
    mock_commands_map_builder.return_value.build.return_value = commands_map
    evaluation = successful_evaluation_mock()
    mock_build_runner.return_value.evaluate.return_value = evaluation

    result = cli_runner.invoke(statue_cli, ["run", context_flag, CONTEXT1])

    assert result.exit_code == 0, f"Failed with exception: {result.exception}"
    assert result.output == DEFAULT_EVALUATION_STRING
    mock_commands_map_builder.assert_called_once_with(
        **run_flags(configuration, contexts=[context])
    )
    mock_commands_map_builder.return_value.build.assert_called_once_with()
    mock_build_runner.assert_called_once_with("SYNC")
    mock_build_runner.return_value.evaluate.assert_called_once_with(commands_map)
    configuration.cache.save_evaluation.assert_called_once_with(evaluation)
    evaluation.save_as_json.assert_not_called()
    mock_evaluation_string.assert_called_once_with(evaluation, verbosity=NORMAL)


@pytest.mark.parametrize("allow_flag", ["-a", "--allow"])
def test_run_cli_with_allowed_command(
    allow_flag,
    cli_runner,
    mock_build_configuration_from_file,
    mock_commands_map_builder,
    mock_build_runner,
    mock_evaluation_string,
    mock_evaluation_summary_string,
):
    commands_builders = [
        command_builder_mock(COMMAND1),
        command_builder_mock(COMMAND2),
        command_builder_mock(COMMAND3),
    ]
    configuration = mock_build_configuration_from_file.return_value
    configuration.commands_repository = commands_builders
    commands_map = mock.MagicMock()
    commands_map.__len__.return_value = 3
    commands_map.command_names = [COMMAND1, COMMAND2, COMMAND3]
    mock_commands_map_builder.return_value.build.return_value = commands_map
    evaluation = successful_evaluation_mock()
    mock_build_runner.return_value.evaluate.return_value = evaluation

    result = cli_runner.invoke(statue_cli, ["run", allow_flag, COMMAND2])

    assert result.exit_code == 0, f"Failed with exception: {result.exception}"
    assert result.output == DEFAULT_EVALUATION_STRING
    mock_commands_map_builder.assert_called_once_with(
        **run_flags(configuration, allowed_commands=[COMMAND2])
    )
    mock_commands_map_builder.return_value.build.assert_called_once_with()
    mock_build_runner.assert_called_once_with("SYNC")
    mock_build_runner.return_value.evaluate.assert_called_once_with(commands_map)
    configuration.cache.save_evaluation.assert_called_once_with(evaluation)
    evaluation.save_as_json.assert_not_called()
    mock_evaluation_string.assert_called_once_with(evaluation, verbosity=NORMAL)


@pytest.mark.parametrize("deny_flag", ["-d", "--deny"])
def test_run_cli_with_denied_command(
    deny_flag,
    cli_runner,
    mock_build_configuration_from_file,
    mock_commands_map_builder,
    mock_build_runner,
    mock_evaluation_string,
    mock_evaluation_summary_string,
):
    commands_builders = [
        command_builder_mock(COMMAND1),
        command_builder_mock(COMMAND2),
        command_builder_mock(COMMAND3),
    ]
    configuration = mock_build_configuration_from_file.return_value
    configuration.commands_repository = commands_builders
    commands_map = mock.MagicMock()
    commands_map.__len__.return_value = 3
    commands_map.command_names = [COMMAND1, COMMAND2, COMMAND3]
    mock_commands_map_builder.return_value.build.return_value = commands_map
    evaluation = successful_evaluation_mock()
    mock_build_runner.return_value.evaluate.return_value = evaluation

    result = cli_runner.invoke(statue_cli, ["run", deny_flag, COMMAND2])

    assert result.exit_code == 0, f"Failed with exception: {result.exception}"
    assert result.output == DEFAULT_EVALUATION_STRING
    mock_commands_map_builder.assert_called_once_with(
        **run_flags(configuration, denied_commands=[COMMAND2])
    )
    mock_commands_map_builder.return_value.build.assert_called_once_with()
    mock_build_runner.assert_called_once_with("SYNC")
    mock_build_runner.return_value.evaluate.assert_called_once_with(commands_map)
    configuration.cache.save_evaluation.assert_called_once_with(evaluation)
    evaluation.save_as_json.assert_not_called()
    mock_evaluation_string.assert_called_once_with(evaluation, verbosity=NORMAL)


@pytest.mark.parametrize("previous_flag", ["-p", "--previous"])
def test_run_cli_on_previous_evaluation(
    previous_flag,
    cli_runner,
    mock_build_configuration_from_file,
    mock_commands_map_builder,
    mock_build_runner,
    mock_evaluation_string,
    mock_evaluation_summary_string,
):
    previous = 3
    commands_builders = [
        command_builder_mock(COMMAND1),
        command_builder_mock(COMMAND2),
        command_builder_mock(COMMAND3),
    ]
    configuration = mock_build_configuration_from_file.return_value
    configuration.commands_repository = commands_builders
    commands_map = mock.MagicMock()
    commands_map.__len__.return_value = 3
    commands_map.command_names = [COMMAND1, COMMAND2, COMMAND3]
    mock_commands_map_builder.return_value.build.return_value = commands_map
    evaluation = successful_evaluation_mock()
    mock_build_runner.return_value.evaluate.return_value = evaluation

    result = cli_runner.invoke(statue_cli, ["run", previous_flag, previous])

    assert result.exit_code == 0, f"Failed with exception: {result.exception}"
    assert result.output == DEFAULT_EVALUATION_STRING
    mock_commands_map_builder.assert_called_once_with(
        **run_flags(configuration, previous=previous)
    )
    mock_commands_map_builder.return_value.build.assert_called_once_with()
    mock_build_runner.assert_called_once_with("SYNC")
    mock_build_runner.return_value.evaluate.assert_called_once_with(commands_map)
    configuration.cache.save_evaluation.assert_called_once_with(evaluation)
    evaluation.save_as_json.assert_not_called()
    mock_evaluation_string.assert_called_once_with(evaluation, verbosity=NORMAL)


@pytest.mark.parametrize("recent_flag", ["-r", "--recent"])
def test_run_cli_on_recent_evaluation(
    recent_flag,
    cli_runner,
    mock_build_configuration_from_file,
    mock_commands_map_builder,
    mock_build_runner,
    mock_evaluation_string,
    mock_evaluation_summary_string,
):
    commands_builders = [
        command_builder_mock(COMMAND1),
        command_builder_mock(COMMAND2),
        command_builder_mock(COMMAND3),
    ]
    configuration = mock_build_configuration_from_file.return_value
    configuration.commands_repository = commands_builders
    commands_map = mock.MagicMock()
    commands_map.__len__.return_value = 3
    commands_map.command_names = [COMMAND1, COMMAND2, COMMAND3]
    mock_commands_map_builder.return_value.build.return_value = commands_map
    evaluation = successful_evaluation_mock()
    mock_build_runner.return_value.evaluate.return_value = evaluation

    result = cli_runner.invoke(statue_cli, ["run", recent_flag])

    assert result.exit_code == 0, f"Failed with exception: {result.exception}"
    assert result.output == DEFAULT_EVALUATION_STRING
    mock_commands_map_builder.assert_called_once_with(
        **run_flags(configuration, previous=1)
    )
    mock_commands_map_builder.return_value.build.assert_called_once_with()
    mock_build_runner.assert_called_once_with("SYNC")
    mock_build_runner.return_value.evaluate.assert_called_once_with(commands_map)
    configuration.cache.save_evaluation.assert_called_once_with(evaluation)
    evaluation.save_as_json.assert_not_called()
    mock_evaluation_string.assert_called_once_with(evaluation, verbosity=NORMAL)


@pytest.mark.parametrize("failed_flag", ["-f", "--failed"])
def test_run_cli_on_failed_evaluation(
    failed_flag,
    cli_runner,
    mock_build_configuration_from_file,
    mock_commands_map_builder,
    mock_build_runner,
    mock_evaluation_string,
    mock_evaluation_summary_string,
):
    commands_builders = [
        command_builder_mock(COMMAND1),
        command_builder_mock(COMMAND2),
        command_builder_mock(COMMAND3),
    ]
    configuration = mock_build_configuration_from_file.return_value
    configuration.commands_repository = commands_builders
    commands_map = mock.MagicMock()
    commands_map.__len__.return_value = 3
    commands_map.command_names = [COMMAND1, COMMAND2, COMMAND3]
    mock_commands_map_builder.return_value.build.return_value = commands_map
    evaluation = successful_evaluation_mock()
    mock_build_runner.return_value.evaluate.return_value = evaluation

    result = cli_runner.invoke(statue_cli, ["run", failed_flag])

    assert result.exit_code == 0, f"Failed with exception: {result.exception}"
    assert result.output == DEFAULT_EVALUATION_STRING
    mock_commands_map_builder.assert_called_once_with(
        **run_flags(configuration, failed=True)
    )
    mock_commands_map_builder.return_value.build.assert_called_once_with()
    mock_build_runner.assert_called_once_with("SYNC")
    mock_build_runner.return_value.evaluate.assert_called_once_with(commands_map)
    configuration.cache.save_evaluation.assert_called_once_with(evaluation)
    evaluation.save_as_json.assert_not_called()
    mock_evaluation_string.assert_called_once_with(evaluation, verbosity=NORMAL)


@pytest.mark.parametrize("failed_only_flag", ["-fo", "--failed-only"])
def test_run_cli_on_failed_only_evaluation(
    failed_only_flag,
    cli_runner,
    mock_build_configuration_from_file,
    mock_commands_map_builder,
    mock_build_runner,
    mock_evaluation_string,
    mock_evaluation_summary_string,
):
    commands_builders = [
        command_builder_mock(COMMAND1),
        command_builder_mock(COMMAND2),
        command_builder_mock(COMMAND3),
    ]
    configuration = mock_build_configuration_from_file.return_value
    configuration.commands_repository = commands_builders
    commands_map = mock.MagicMock()
    commands_map.__len__.return_value = 3
    commands_map.command_names = [COMMAND1, COMMAND2, COMMAND3]
    mock_commands_map_builder.return_value.build.return_value = commands_map
    evaluation = successful_evaluation_mock()
    mock_build_runner.return_value.evaluate.return_value = evaluation

    result = cli_runner.invoke(statue_cli, ["run", failed_only_flag])

    assert result.exit_code == 0, f"Failed with exception: {result.exception}"
    assert result.output == DEFAULT_EVALUATION_STRING
    mock_commands_map_builder.assert_called_once_with(
        **run_flags(configuration, failed_only=True)
    )
    mock_commands_map_builder.return_value.build.assert_called_once_with()
    mock_build_runner.assert_called_once_with("SYNC")
    mock_build_runner.return_value.evaluate.assert_called_once_with(commands_map)
    configuration.cache.save_evaluation.assert_called_once_with(evaluation)
    evaluation.save_as_json.assert_not_called()
    mock_evaluation_string.assert_called_once_with(evaluation, verbosity=NORMAL)


def test_run_cli_with_empty_commands_map(
    cli_runner,
    mock_build_configuration_from_file,
    mock_commands_map_builder,
    mock_build_runner,
    mock_evaluation_string,
    mock_evaluation_summary_string,
):
    configuration = mock_build_configuration_from_file.return_value
    commands_map = mock.MagicMock()
    commands_map.__len__.return_value = 0
    mock_commands_map_builder.return_value.build.return_value = commands_map

    result = cli_runner.invoke(statue_cli, ["run"])

    assert result.exit_code == 0, f"Failed with exception: {result.exception}"
    assert result.output == "No commands to run.\n"
    mock_commands_map_builder.assert_called_once_with(**run_flags(configuration))
    mock_commands_map_builder.return_value.build.assert_called_once_with()
    mock_build_runner.assert_not_called()
    configuration.cache.save_evaluation.assert_not_called()
    mock_evaluation_string.assert_not_called()


def test_run_cli_verbosely(
    cli_runner,
    mock_build_configuration_from_file,
    mock_commands_map_builder,
    mock_build_runner,
    mock_evaluation_string,
    mock_evaluation_summary_string,
):
    commands_builders = [
        command_builder_mock(COMMAND1),
        command_builder_mock(COMMAND2),
        command_builder_mock(COMMAND3),
    ]
    configuration = mock_build_configuration_from_file.return_value
    configuration.commands_repository = commands_builders
    commands_map = mock.MagicMock()
    commands_map.__len__.return_value = 3
    commands_map.command_names = [COMMAND1, COMMAND2, COMMAND3]
    mock_commands_map_builder.return_value.build.return_value = commands_map
    evaluation = successful_evaluation_mock()
    mock_build_runner.return_value.evaluate.return_value = evaluation

    result = cli_runner.invoke(statue_cli, ["run", "--verbose"])

    assert result.exit_code == 0, f"Failed with exception: {result.exception}"
    assert result.output == (
        "Running evaluation in sync mode\n"
        "##############\n"
        "# Evaluation #\n"
        "##############\n"
        "This is a pretty evaluation string\n"
        "\n"
        "###########\n"
        "# Summary #\n"
        "###########\n"
        "\n"
        "This is a pretty evaluation summary string\n"
    )
    mock_commands_map_builder.assert_called_once_with(**run_flags(configuration))
    mock_commands_map_builder.return_value.build.assert_called_once_with()
    mock_build_runner.assert_called_once_with("SYNC")
    mock_build_runner.return_value.evaluate.assert_called_once_with(commands_map)
    configuration.cache.save_evaluation.assert_called_once_with(evaluation)
    evaluation.save_as_json.assert_not_called()
    mock_evaluation_string.assert_called_once_with(evaluation, verbosity=VERBOSE)


def test_run_cli_silently(
    cli_runner,
    mock_build_configuration_from_file,
    mock_commands_map_builder,
    mock_build_runner,
    mock_evaluation_string,
    mock_evaluation_summary_string,
):
    commands_builders = [
        command_builder_mock(COMMAND1),
        command_builder_mock(COMMAND2),
        command_builder_mock(COMMAND3),
    ]
    configuration = mock_build_configuration_from_file.return_value
    configuration.commands_repository = commands_builders
    commands_map = mock.MagicMock()
    commands_map.__len__.return_value = 3
    commands_map.command_names = [COMMAND1, COMMAND2, COMMAND3]
    mock_commands_map_builder.return_value.build.return_value = commands_map
    evaluation = successful_evaluation_mock()
    mock_build_runner.return_value.evaluate.return_value = evaluation

    result = cli_runner.invoke(statue_cli, ["run", "--silent"])

    assert result.exit_code == 0, f"Failed with exception: {result.exception}"
    assert result.output == "\nThis is a pretty evaluation summary string\n"
    mock_commands_map_builder.assert_called_once_with(**run_flags(configuration))
    mock_commands_map_builder.return_value.build.assert_called_once_with()
    mock_build_runner.assert_called_once_with("SYNC")
    mock_build_runner.return_value.evaluate.assert_called_once_with(commands_map)
    configuration.cache.save_evaluation.assert_called_once_with(evaluation)
    evaluation.save_as_json.assert_not_called()
    mock_evaluation_string.assert_not_called()


@pytest.mark.parametrize("install_flag", ["-i", "--install"])
def test_run_cli_with_install_flag(
    install_flag,
    cli_runner,
    mock_build_configuration_from_file,
    mock_commands_map_builder,
    mock_build_runner,
    mock_evaluation_string,
    mock_evaluation_summary_string,
):
    command_builder1, command_builder2, command_builder3 = (
        command_builder_mock(COMMAND1, installed=False),
        command_builder_mock(COMMAND2),
        command_builder_mock(COMMAND3, installed=False),
    )
    configuration = mock_build_configuration_from_file.return_value
    configuration.commands_repository = [
        command_builder1,
        command_builder2,
        command_builder3,
    ]
    commands_map = mock.MagicMock()
    commands_map.__len__.return_value = 3
    commands_map.command_names = [COMMAND1, COMMAND2, COMMAND3]
    mock_commands_map_builder.return_value.build.return_value = commands_map
    evaluation = successful_evaluation_mock()
    mock_build_runner.return_value.evaluate.return_value = evaluation

    result = cli_runner.invoke(statue_cli, ["run", install_flag])

    assert result.exit_code == 0, f"Failed with exception: {result.exception}"
    assert result.output == DEFAULT_EVALUATION_STRING
    mock_commands_map_builder.assert_called_once_with(**run_flags(configuration))
    mock_commands_map_builder.return_value.build.assert_called_once_with()
    command_builder1.update_to_version.assert_called_once_with(verbosity=NORMAL)
    command_builder3.update_to_version.assert_called_once_with(verbosity=NORMAL)
    command_builder2.update_to_version.assert_not_called()
    mock_build_runner.assert_called_once_with("SYNC")
    mock_build_runner.return_value.evaluate.assert_called_once_with(commands_map)
    configuration.cache.save_evaluation.assert_called_once_with(evaluation)
    evaluation.save_as_json.assert_not_called()
    mock_evaluation_string.assert_called_once_with(evaluation, verbosity=NORMAL)


def test_run_cli_without_cache(
    cli_runner,
    mock_build_configuration_from_file,
    mock_commands_map_builder,
    mock_build_runner,
    mock_evaluation_string,
    mock_evaluation_summary_string,
):
    commands_builders = [
        command_builder_mock(COMMAND1),
        command_builder_mock(COMMAND2),
        command_builder_mock(COMMAND3),
    ]
    configuration = mock_build_configuration_from_file.return_value
    configuration.commands_repository = commands_builders
    commands_map = mock.MagicMock()
    commands_map.__len__.return_value = 3
    commands_map.command_names = [COMMAND1, COMMAND2, COMMAND3]
    mock_commands_map_builder.return_value.build.return_value = commands_map
    evaluation = successful_evaluation_mock()
    mock_build_runner.return_value.evaluate.return_value = evaluation

    result = cli_runner.invoke(statue_cli, ["run", "--no-cache"])

    assert result.exit_code == 0, f"Failed with exception: {result.exception}"
    assert result.output == DEFAULT_EVALUATION_STRING
    mock_commands_map_builder.assert_called_once_with(**run_flags(configuration))
    mock_commands_map_builder.return_value.build.assert_called_once_with()
    mock_build_runner.assert_called_once_with("SYNC")
    mock_build_runner.return_value.evaluate.assert_called_once_with(commands_map)
    configuration.cache.save_evaluation.assert_not_called()
    evaluation.save_as_json.assert_not_called()
    mock_evaluation_string.assert_called_once_with(evaluation, verbosity=NORMAL)


def test_run_cli_with_output_path(
    tmp_path,
    cli_runner,
    mock_build_configuration_from_file,
    mock_commands_map_builder,
    mock_build_runner,
    mock_evaluation_string,
    mock_evaluation_summary_string,
):
    output_path = tmp_path / "eval.json"

    commands_builders = [
        command_builder_mock(COMMAND1),
        command_builder_mock(COMMAND2),
        command_builder_mock(COMMAND3),
    ]
    configuration = mock_build_configuration_from_file.return_value
    configuration.commands_repository = commands_builders
    commands_map = mock.MagicMock()
    commands_map.__len__.return_value = 3
    commands_map.command_names = [COMMAND1, COMMAND2, COMMAND3]
    mock_commands_map_builder.return_value.build.return_value = commands_map
    evaluation = successful_evaluation_mock()
    mock_build_runner.return_value.evaluate.return_value = evaluation

    result = cli_runner.invoke(statue_cli, ["run", "-o", str(output_path)])

    assert result.exit_code == 0, f"Failed with exception: {result.exception}"
    assert result.output == DEFAULT_EVALUATION_STRING
    mock_commands_map_builder.assert_called_once_with(**run_flags(configuration))
    mock_commands_map_builder.return_value.build.assert_called_once_with()
    mock_build_runner.assert_called_once_with("SYNC")
    mock_build_runner.return_value.evaluate.assert_called_once_with(commands_map)
    configuration.cache.save_evaluation.assert_called_once_with(evaluation)
    evaluation.save_as_json.assert_called_once_with(output_path)
    mock_evaluation_string.assert_called_once_with(evaluation, verbosity=NORMAL)


@pytest.mark.parametrize("runner_mode", RunnerMode)
def test_run_cli_with_mode(
    runner_mode,
    cli_runner,
    mock_build_configuration_from_file,
    mock_commands_map_builder,
    mock_build_runner,
    mock_evaluation_string,
    mock_evaluation_summary_string,
):
    commands_builders = [
        command_builder_mock(COMMAND1),
        command_builder_mock(COMMAND2),
        command_builder_mock(COMMAND3),
    ]
    configuration = mock_build_configuration_from_file.return_value
    configuration.commands_repository = commands_builders
    commands_map = mock.MagicMock()
    commands_map.__len__.return_value = 3
    commands_map.command_names = [COMMAND1, COMMAND2, COMMAND3]
    mock_commands_map_builder.return_value.build.return_value = commands_map
    evaluation = successful_evaluation_mock()
    mock_build_runner.return_value.evaluate.return_value = evaluation

    result = cli_runner.invoke(statue_cli, ["run", "--mode", runner_mode.name])

    assert result.exit_code == 0, f"Failed with exception: {result.exception}"
    assert result.output == DEFAULT_EVALUATION_STRING
    mock_commands_map_builder.assert_called_once_with(**run_flags(configuration))
    mock_commands_map_builder.return_value.build.assert_called_once_with()
    mock_build_runner.assert_called_once_with(runner_mode.name)
    mock_build_runner.return_value.evaluate.assert_called_once_with(commands_map)
    configuration.cache.save_evaluation.assert_called_once_with(evaluation)
    evaluation.save_as_json.assert_not_called()
    mock_evaluation_string.assert_called_once_with(evaluation, verbosity=NORMAL)


# Failed runs


def test_run_cli_fail_due_to_unknown_context(
    cli_runner,
    mock_build_configuration_from_file,
    mock_commands_map_builder,
    mock_build_runner,
    mock_evaluation_string,
    mock_evaluation_summary_string,
):
    mock_commands_map_builder.side_effect = UnknownContext(CONTEXT1)

    result = cli_runner.invoke(statue_cli, ["run", "-c", CONTEXT1])

    assert (
        result.exit_code == 1
    ), f"Exit code is different than expected. Exception: {result.exception}"
    assert result.output == 'Could not find context named "context1"\n'

    mock_build_runner.assert_not_called()
    mock_evaluation_string.assert_not_called()


def test_run_cli_fail_due_to_commands_map_builder_error(
    cli_runner,
    mock_build_configuration_from_file,
    mock_commands_map_builder,
    mock_build_runner,
    mock_evaluation_string,
    mock_evaluation_summary_string,
):
    message = "This is a message"
    mock_commands_map_builder.side_effect = CommandsMapBuilderError(message)

    result = cli_runner.invoke(statue_cli, ["run"])

    assert (
        result.exit_code == 1
    ), f"Exit code is different than expected. Exception: {result.exception}"
    assert result.output == f"{message}\n"

    mock_build_runner.assert_not_called()
    mock_evaluation_string.assert_not_called()


def test_run_cli_with_failed_evaluation(
    cli_runner,
    mock_build_configuration_from_file,
    mock_commands_map_builder,
    mock_build_runner,
    mock_evaluation_string,
    mock_evaluation_summary_string,
):
    commands_builders = [
        command_builder_mock(COMMAND1),
        command_builder_mock(COMMAND2),
        command_builder_mock(COMMAND3),
    ]
    configuration = mock_build_configuration_from_file.return_value
    configuration.commands_repository = commands_builders
    commands_map = mock.MagicMock()
    commands_map.__len__.return_value = 3
    commands_map.command_names = [COMMAND1, COMMAND2, COMMAND3]
    mock_commands_map_builder.return_value.build.return_value = commands_map
    evaluation = failed_evaluation_mock()
    mock_build_runner.return_value.evaluate.return_value = evaluation

    result = cli_runner.invoke(statue_cli, ["run"])

    assert (
        result.exit_code == 1
    ), f"Got unexpected exit error. exception: {result.exception}"
    assert result.output == DEFAULT_EVALUATION_STRING
    mock_commands_map_builder.assert_called_once_with(**run_flags(configuration))
    mock_commands_map_builder.return_value.build.assert_called_once_with()
    mock_build_runner.assert_called_once_with("SYNC")
    mock_build_runner.return_value.evaluate.assert_called_once_with(commands_map)
    configuration.cache.save_evaluation.assert_called_once_with(evaluation)
    evaluation.save_as_json.assert_not_called()
    mock_evaluation_string.assert_called_once_with(evaluation, verbosity=NORMAL)


def test_run_cli_fail_in_installed_commands(
    cli_runner,
    mock_build_configuration_from_file,
    mock_commands_map_builder,
    mock_build_runner,
    mock_evaluation_string,
    mock_evaluation_summary_string,
):
    command_builder1, command_builder2, command_builder3 = (
        command_builder_mock(COMMAND1, installed=False),
        command_builder_mock(COMMAND2),
        command_builder_mock(COMMAND3, installed=False),
    )
    configuration = mock_build_configuration_from_file.return_value
    configuration.commands_repository = [
        command_builder1,
        command_builder2,
        command_builder3,
    ]
    commands_map = mock.MagicMock()
    commands_map.__len__.return_value = 3
    commands_map.command_names = [COMMAND1, COMMAND2, COMMAND3]
    mock_commands_map_builder.return_value.build.return_value = commands_map

    result = cli_runner.invoke(statue_cli, ["run"])

    assert (
        result.exit_code == 1
    ), f"Got unexpected exit error. exception: {result.exception}"
    assert result.output == (
        f"The following commands are not installed correctly: {COMMAND1}, {COMMAND3}\n"
        "Consider using the '-i' flag in order to install missing commands before "
        "running\n"
    )
    mock_commands_map_builder.assert_called_once_with(**run_flags(configuration))
    mock_commands_map_builder.return_value.build.assert_called_once_with()
    command_builder1.update_to_version.assert_not_called()
    command_builder3.update_to_version.assert_not_called()
    command_builder2.update_to_version.assert_not_called()
    mock_build_runner.assert_not_called()
    configuration.cache.save_evaluation.assert_not_called()
    mock_evaluation_string.assert_not_called()
