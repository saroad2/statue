from unittest import mock

import click
from pytest_cases import THIS_MODULE, fixture, parametrize, parametrize_with_cases

from statue.cache import Cache
from statue.cli import statue as statue_cli
from statue.command import Command
from statue.constants import SOURCES
from statue.evaluation import CommandEvaluation, Evaluation, SourceEvaluation
from statue.exceptions import (
    CommandExecutionError,
    MissingConfiguration,
    UnknownContext,
)
from statue.verbosity import DEFAULT_VERBOSITY, SILENT
from tests.constants import (
    COMMAND1,
    COMMAND2,
    COMMAND3,
    COMMAND4,
    COMMAND5,
    COMMAND_HELP_STRING1,
    COMMAND_HELP_STRING2,
    COMMAND_HELP_STRING3,
    COMMAND_HELP_STRING4,
    COMMAND_HELP_STRING5,
    NOT_EXISTING_CONTEXT,
    SOURCE1,
    SOURCE2,
)
from tests.util import assert_calls

NONE_SILENT_PRINT_INTRO = [
    "##############",
    "# Evaluation #",
    "##############",
    "",
    "###########",
    "# Summary #",
    "###########",
    "",
]

COMMAND_INSTANCE1 = Command(COMMAND1, help=COMMAND_HELP_STRING1)
COMMAND_INSTANCE2 = Command(COMMAND2, help=COMMAND_HELP_STRING2)
COMMAND_INSTANCE3 = Command(COMMAND3, help=COMMAND_HELP_STRING3)
COMMAND_INSTANCE4 = Command(COMMAND4, help=COMMAND_HELP_STRING4)
COMMAND_INSTANCE5 = Command(COMMAND5, help=COMMAND_HELP_STRING5)

COMMANDS_MAP = {
    SOURCE1: [COMMAND_INSTANCE1, COMMAND_INSTANCE2],
    SOURCE2: [COMMAND_INSTANCE3, COMMAND_INSTANCE4, COMMAND_INSTANCE5],
}
SUCCESSFUL_EVALUATION = Evaluation(
    {
        SOURCE1: SourceEvaluation(
            [
                CommandEvaluation(command=COMMAND_INSTANCE1, success=True),
                CommandEvaluation(command=COMMAND_INSTANCE2, success=True),
            ]
        ),
        SOURCE2: SourceEvaluation(
            [
                CommandEvaluation(command=COMMAND_INSTANCE3, success=True),
                CommandEvaluation(command=COMMAND_INSTANCE4, success=True),
                CommandEvaluation(command=COMMAND_INSTANCE5, success=True),
            ]
        ),
    }
)
ONE_ERROR_EVALUATION = Evaluation(
    {
        SOURCE1: SourceEvaluation(
            [
                CommandEvaluation(command=COMMAND_INSTANCE1, success=True),
                CommandEvaluation(command=COMMAND_INSTANCE2, success=True),
            ]
        ),
        SOURCE2: SourceEvaluation(
            [
                CommandEvaluation(command=COMMAND_INSTANCE3, success=True),
                CommandEvaluation(command=COMMAND_INSTANCE4, success=False),
                CommandEvaluation(command=COMMAND_INSTANCE5, success=True),
            ]
        ),
    }
)
ONE_SOURCE_TWO_ERRORS_EVALUATION = Evaluation(
    {
        SOURCE1: SourceEvaluation(
            [
                CommandEvaluation(command=COMMAND_INSTANCE1, success=True),
                CommandEvaluation(command=COMMAND_INSTANCE2, success=True),
            ]
        ),
        SOURCE2: SourceEvaluation(
            [
                CommandEvaluation(command=COMMAND_INSTANCE3, success=True),
                CommandEvaluation(command=COMMAND_INSTANCE4, success=False),
                CommandEvaluation(command=COMMAND_INSTANCE5, success=False),
            ]
        ),
    }
)
TWO_SOURCES_TWO_ERRORS_EVALUATION = Evaluation(
    {
        SOURCE1: SourceEvaluation(
            [
                CommandEvaluation(command=COMMAND_INSTANCE1, success=True),
                CommandEvaluation(command=COMMAND_INSTANCE2, success=False),
            ]
        ),
        SOURCE2: SourceEvaluation(
            [
                CommandEvaluation(command=COMMAND_INSTANCE3, success=True),
                CommandEvaluation(command=COMMAND_INSTANCE4, success=False),
                CommandEvaluation(command=COMMAND_INSTANCE5, success=True),
            ]
        ),
    }
)
ALL_FAILURE_EVALUATION = Evaluation(
    {
        SOURCE1: SourceEvaluation(
            [
                CommandEvaluation(command=COMMAND_INSTANCE1, success=False),
                CommandEvaluation(command=COMMAND_INSTANCE2, success=False),
            ]
        ),
        SOURCE2: SourceEvaluation(
            [
                CommandEvaluation(command=COMMAND_INSTANCE3, success=False),
                CommandEvaluation(command=COMMAND_INSTANCE4, success=False),
                CommandEvaluation(command=COMMAND_INSTANCE5, success=False),
            ]
        ),
    }
)
EVALUATIONS = [
    (SUCCESSFUL_EVALUATION, 0, ["Statue finished successfully!", ""]),
    (
        ONE_ERROR_EVALUATION,
        1,
        [
            "Statue has failed on the following commands:",
            "",
            "source2:",
            "\tcommand4",
            "",
        ],
    ),
    (
        ONE_SOURCE_TWO_ERRORS_EVALUATION,
        1,
        [
            "Statue has failed on the following commands:",
            "",
            "source2:",
            "\tcommand4, command5",
            "",
        ],
    ),
    (
        TWO_SOURCES_TWO_ERRORS_EVALUATION,
        1,
        [
            "Statue has failed on the following commands:",
            "",
            "source1:",
            "\tcommand2",
            "source2:",
            "\tcommand4",
            "",
        ],
    ),
    (
        ALL_FAILURE_EVALUATION,
        1,
        [
            "Statue has failed on the following commands:",
            "",
            "source1:",
            "\tcommand1, command2",
            "source2:",
            "\tcommand3, command4, command5",
            "",
        ],
    ),
]


@fixture
def mock_read_commands_map(mocker):
    return mocker.patch("statue.cli.run.read_commands_map")


@fixture
def mock_evaluate_commands_map(mocker):
    return mocker.patch("statue.cli.run.evaluate_commands_map")


@fixture
def mock_cache_recent_evaluation_path(mocker):
    return mocker.patch.object(Cache, "recent_evaluation_path").return_value


@fixture
def mock_evaluation_load_from_file(mocker):
    return mocker.patch.object(Evaluation, "load_from_file")


@fixture
def mock_evaluation_save_as_json(mocker):
    return mocker.patch.object(Evaluation, "save_as_json")


@parametrize(argnames="evaluation, exit_code, prints", argvalues=EVALUATIONS)
def case_simple_run(
    evaluation,
    exit_code,
    prints,
    mock_read_commands_map,
    mock_evaluate_commands_map,
    mock_cache_recent_evaluation_path,
    mock_evaluation_save_as_json,
):
    extra_args = []

    mock_read_commands_map.return_value = COMMANDS_MAP
    mock_evaluate_commands_map.return_value = evaluation

    yield extra_args, exit_code, NONE_SILENT_PRINT_INTRO + prints
    mock_read_commands_map.assert_called_with(
        (), contexts=(), allow_list=(), deny_list=()
    )
    mock_evaluate_commands_map.assert_called_once_with(
        commands_map=COMMANDS_MAP, print_method=click.echo, verbosity=DEFAULT_VERBOSITY
    )
    mock_evaluation_save_as_json.assert_called_once_with(
        mock_cache_recent_evaluation_path
    )


@parametrize(argnames="evaluation, exit_code, prints", argvalues=EVALUATIONS)
def case_run_silently(
    evaluation,
    exit_code,
    prints,
    mock_read_commands_map,
    mock_evaluate_commands_map,
    mock_cache_recent_evaluation_path,
    mock_evaluation_save_as_json,
):
    extra_args = ["--silent"]

    mock_read_commands_map.return_value = COMMANDS_MAP
    mock_evaluate_commands_map.return_value = evaluation

    yield extra_args, exit_code, [""] + prints
    mock_read_commands_map.assert_called_with(
        (), contexts=(), allow_list=(), deny_list=()
    )
    mock_evaluate_commands_map.assert_called_with(
        commands_map=COMMANDS_MAP, print_method=click.echo, verbosity=SILENT
    )
    mock_evaluation_save_as_json.assert_called_once_with(
        mock_cache_recent_evaluation_path
    )


@parametrize(argnames="evaluation, exit_code, prints", argvalues=EVALUATIONS)
def case_run_failed_with_non_existing_last_evaluation(
    evaluation,
    exit_code,
    prints,
    mock_read_commands_map,
    mock_evaluate_commands_map,
    mock_cache_recent_evaluation_path,
    mock_evaluation_save_as_json,
):
    extra_args = ["--failed"]

    mock_cache_recent_evaluation_path.exists.return_value = False
    mock_read_commands_map.return_value = COMMANDS_MAP
    mock_evaluate_commands_map.return_value = evaluation

    yield extra_args, exit_code, NONE_SILENT_PRINT_INTRO + prints
    mock_read_commands_map.assert_called_with(
        (), contexts=(), allow_list=(), deny_list=()
    )
    mock_evaluate_commands_map.assert_called_with(
        commands_map=COMMANDS_MAP, print_method=click.echo, verbosity=DEFAULT_VERBOSITY
    )
    mock_evaluation_save_as_json.assert_called_once_with(
        mock_cache_recent_evaluation_path
    )


@parametrize(argnames="evaluation, exit_code, prints", argvalues=EVALUATIONS)
def case_run_failed_with_successful_last_evaluation(
    evaluation,
    exit_code,
    prints,
    mock_read_commands_map,
    mock_evaluate_commands_map,
    mock_cache_recent_evaluation_path,
    mock_evaluation_load_from_file,
    mock_evaluation_save_as_json,
):
    extra_args = ["--failed"]

    mock_cache_recent_evaluation_path.exists.return_value = True
    mock_evaluation_load_from_file.return_value = SUCCESSFUL_EVALUATION
    mock_read_commands_map.return_value = COMMANDS_MAP
    mock_evaluate_commands_map.return_value = evaluation

    yield extra_args, exit_code, NONE_SILENT_PRINT_INTRO + prints
    mock_read_commands_map.assert_called_with(
        (), contexts=(), allow_list=(), deny_list=()
    )
    mock_evaluate_commands_map.assert_called_with(
        commands_map=COMMANDS_MAP, print_method=click.echo, verbosity=DEFAULT_VERBOSITY
    )
    mock_evaluation_save_as_json.assert_called_once_with(
        mock_cache_recent_evaluation_path
    )


@parametrize(argnames="evaluation, exit_code, prints", argvalues=EVALUATIONS)
def case_run_failed_with_failure_last_evaluation(
    evaluation,
    exit_code,
    prints,
    mock_read_commands_map,
    mock_evaluate_commands_map,
    mock_cache_recent_evaluation_path,
    mock_evaluation_load_from_file,
    mock_evaluation_save_as_json,
):
    extra_args = ["--failed"]

    mock_cache_recent_evaluation_path.exists.return_value = True
    mock_evaluation_load_from_file.return_value = ALL_FAILURE_EVALUATION
    mock_evaluate_commands_map.return_value = evaluation

    yield extra_args, exit_code, NONE_SILENT_PRINT_INTRO + prints
    mock_read_commands_map.assert_not_called()
    mock_evaluate_commands_map.assert_called_with(
        commands_map=COMMANDS_MAP, print_method=click.echo, verbosity=DEFAULT_VERBOSITY
    )
    mock_evaluation_save_as_json.assert_called_once_with(
        mock_cache_recent_evaluation_path
    )


@parametrize(argnames="evaluation, exit_code, prints", argvalues=EVALUATIONS)
def case_run_and_install(
    evaluation,
    exit_code,
    prints,
    mock_read_commands_map,
    mock_evaluate_commands_map,
    mock_cache_recent_evaluation_path,
    mock_evaluation_save_as_json,
    mock_available_packages,
    mock_subprocess,
):
    extra_args = ["-i"]

    mock_read_commands_map.return_value = COMMANDS_MAP
    mock_available_packages.return_value = []
    mock_evaluate_commands_map.return_value = evaluation
    installing_intro = [
        f"Installing {COMMAND1}",
        f"Installing {COMMAND2}",
        f"Installing {COMMAND3}",
        f"Installing {COMMAND4}",
        f"Installing {COMMAND5}",
    ]

    yield extra_args, exit_code, installing_intro + NONE_SILENT_PRINT_INTRO + prints
    mock_subprocess.assert_called()
    mock_read_commands_map.assert_called_with(
        (), contexts=(), allow_list=(), deny_list=()
    )
    mock_evaluate_commands_map.assert_called_with(
        commands_map=COMMANDS_MAP, print_method=click.echo, verbosity=DEFAULT_VERBOSITY
    )
    mock_evaluation_save_as_json.assert_called_once_with(
        mock_cache_recent_evaluation_path
    )


@parametrize(argnames="evaluation, exit_code, prints", argvalues=EVALUATIONS)
def case_no_cache(
    evaluation,
    exit_code,
    prints,
    mock_read_commands_map,
    mock_evaluate_commands_map,
    mock_evaluation_save_as_json,
):
    extra_args = ["--no-cache"]

    mock_read_commands_map.return_value = COMMANDS_MAP
    mock_evaluate_commands_map.return_value = evaluation

    yield extra_args, exit_code, NONE_SILENT_PRINT_INTRO + prints
    mock_read_commands_map.assert_called_with(
        (), contexts=(), allow_list=(), deny_list=()
    )
    mock_evaluate_commands_map.assert_called_once_with(
        commands_map=COMMANDS_MAP, print_method=click.echo, verbosity=DEFAULT_VERBOSITY
    )
    mock_evaluation_save_as_json.assert_not_called()


@parametrize(argnames="evaluation, exit_code, prints", argvalues=EVALUATIONS)
def case_save_output(
    evaluation,
    exit_code,
    prints,
    mock_read_commands_map,
    mock_evaluate_commands_map,
    mock_cache_recent_evaluation_path,
    mock_evaluation_save_as_json,
):
    output_path = "/path/to/output"
    extra_args = ["-o", output_path]

    mock_read_commands_map.return_value = COMMANDS_MAP
    mock_evaluate_commands_map.return_value = evaluation

    yield extra_args, exit_code, NONE_SILENT_PRINT_INTRO + prints
    mock_read_commands_map.assert_called_with(
        (), contexts=(), allow_list=(), deny_list=()
    )
    mock_evaluate_commands_map.assert_called_with(
        commands_map=COMMANDS_MAP, print_method=click.echo, verbosity=DEFAULT_VERBOSITY
    )
    assert_calls(
        mock_evaluation_save_as_json,
        [mock.call(mock_cache_recent_evaluation_path), mock.call(output_path)],
    )


@parametrize_with_cases(
    argnames=["extra_args", "exit_code", "prints"], cases=THIS_MODULE
)
def test_run(
    extra_args,
    exit_code,
    prints,
    cli_runner,
    empty_configuration,
):
    result = cli_runner.invoke(statue_cli, ["run", *extra_args])
    assert result.exit_code == exit_code, (
        f"Run should exit with {exit_code}. "
        f"Output: {result.output}. "
        f"Exception: {result.exception}."
    )
    assert result.output.split("\n") == prints, "Run output is different than expected."


def test_read_commands_map_returns_empty_map(
    cli_runner, empty_configuration, mock_read_commands_map, mock_evaluate_commands_map
):
    mock_read_commands_map.return_value = {}
    result = cli_runner.invoke(statue_cli, ["run"])
    assert result.exit_code == 0, "Run should exit with 0."
    mock_evaluate_commands_map.assert_not_called()


def test_read_commands_map_raise_unknown_context_error(
    cli_runner, empty_configuration, mock_read_commands_map
):
    mock_read_commands_map.side_effect = UnknownContext(NOT_EXISTING_CONTEXT)
    result = cli_runner.invoke(statue_cli, ["run"])
    assert result.exit_code == 1, "Run should exit with 1."
    assert result.output.split("\n") == [
        f'Could not find context named "{NOT_EXISTING_CONTEXT}".',
        "",
    ], "Run output is different than expected."


def test_read_commands_map_raise_missing_configuration_error(
    cli_runner, empty_configuration, mock_read_commands_map
):
    mock_read_commands_map.side_effect = MissingConfiguration(SOURCES)
    result = cli_runner.invoke(statue_cli, ["run"])
    assert result.exit_code == 1, "Run should exit with 1."
    assert result.output.split("\n") == [
        '"Run" command cannot be run without a specified source '
        "or a sources section in Statue's configuration.",
        'Please consider running "statue config init" in order to initialize default '
        "configuration.",
        "",
    ], "Run output is different than expected."


def test_evaluate_commands_map_raise_execution_error(
    cli_runner, empty_configuration, mock_read_commands_map, mock_evaluate_commands_map
):
    mock_read_commands_map.return_value = COMMANDS_MAP
    mock_evaluate_commands_map.side_effect = CommandExecutionError(
        command_name=COMMAND1
    )
    result = cli_runner.invoke(statue_cli, ["run"])
    assert result.exit_code == 1, "Run should exit with 1."
    assert result.output == (
        "##############\n"
        "# Evaluation #\n"
        "##############\n"
        'Cannot execute "command1" because it is not installed.\n'
        'Try to rerun with the "-i" flag\n'
    ), "Output is different than expected"
