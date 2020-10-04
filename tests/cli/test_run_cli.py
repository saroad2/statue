import click
from pytest_cases import THIS_MODULE, fixture, parametrize, parametrize_with_cases

from statue.cache import Cache
from statue.cli import statue as statue_cli
from statue.command import Command
from statue.evaluation import CommandEvaluation, Evaluation, SourceEvaluation
from statue.exceptions import UnknownContext
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

NONE_SILENT_PRINT_INTRO = [
    "Evaluation",
    "==========",
    "",
    "Summary",
    "=======",
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
def mock_cache_last_evaluation_path(mocker):
    return mocker.patch.object(Cache, "last_evaluation_path").return_value


@fixture
def mock_evaluation_load_from_file(mocker):
    return mocker.patch.object(Evaluation, "load_from_file")


@fixture
def mock_install_commands_if_missing(mocker):
    return mocker.patch("statue.cli.run.install_commands_if_missing")


@parametrize(argnames="evaluation, exit_code, prints", argvalues=EVALUATIONS)
def case_simple_run(
    evaluation, exit_code, prints, mock_read_commands_map, mock_evaluate_commands_map
):
    extra_args = []

    mock_read_commands_map.return_value = COMMANDS_MAP
    mock_evaluate_commands_map.return_value = evaluation

    yield extra_args, exit_code, NONE_SILENT_PRINT_INTRO + prints
    mock_read_commands_map.assert_called_with(
        (), contexts=(), allow_list=(), deny_list=()
    )
    mock_evaluate_commands_map.assert_called_with(
        commands_map=COMMANDS_MAP, print_method=click.echo, verbosity=DEFAULT_VERBOSITY
    )


@parametrize(argnames="evaluation, exit_code, prints", argvalues=EVALUATIONS)
def case_run_silently(
    evaluation, exit_code, prints, mock_read_commands_map, mock_evaluate_commands_map
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


@parametrize(argnames="evaluation, exit_code, prints", argvalues=EVALUATIONS)
def case_run_failed_with_non_existing_last_evaluation(
    evaluation,
    exit_code,
    prints,
    mock_read_commands_map,
    mock_evaluate_commands_map,
    mock_cache_last_evaluation_path,
):
    extra_args = ["--failed"]

    mock_cache_last_evaluation_path.exists.return_value = False
    mock_read_commands_map.return_value = COMMANDS_MAP
    mock_evaluate_commands_map.return_value = evaluation

    yield extra_args, exit_code, NONE_SILENT_PRINT_INTRO + prints
    mock_read_commands_map.assert_called_with(
        (), contexts=(), allow_list=(), deny_list=()
    )
    mock_evaluate_commands_map.assert_called_with(
        commands_map=COMMANDS_MAP, print_method=click.echo, verbosity=DEFAULT_VERBOSITY
    )


@parametrize(argnames="evaluation, exit_code, prints", argvalues=EVALUATIONS)
def case_run_failed_with_successful_last_evaluation(
    evaluation,
    exit_code,
    prints,
    mock_read_commands_map,
    mock_evaluate_commands_map,
    mock_cache_last_evaluation_path,
    mock_evaluation_load_from_file,
):
    extra_args = ["--failed"]

    mock_cache_last_evaluation_path.exists.return_value = True
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


@parametrize(argnames="evaluation, exit_code, prints", argvalues=EVALUATIONS)
def case_run_failed_with_failure_last_evaluation(
    evaluation,
    exit_code,
    prints,
    mock_read_commands_map,
    mock_evaluate_commands_map,
    mock_cache_last_evaluation_path,
    mock_evaluation_load_from_file,
):
    extra_args = ["--failed"]

    mock_cache_last_evaluation_path.exists.return_value = True
    mock_evaluation_load_from_file.return_value = ALL_FAILURE_EVALUATION
    mock_evaluate_commands_map.return_value = evaluation

    yield extra_args, exit_code, NONE_SILENT_PRINT_INTRO + prints
    mock_read_commands_map.assert_not_called()
    mock_evaluate_commands_map.assert_called_with(
        commands_map=COMMANDS_MAP, print_method=click.echo, verbosity=DEFAULT_VERBOSITY
    )


@parametrize(argnames="evaluation, exit_code, prints", argvalues=EVALUATIONS)
def case_run_and_install(
    evaluation,
    exit_code,
    prints,
    mock_read_commands_map,
    mock_evaluate_commands_map,
    mock_install_commands_if_missing,
):
    extra_args = ["-i"]

    mock_read_commands_map.return_value = COMMANDS_MAP
    mock_evaluate_commands_map.return_value = evaluation

    yield extra_args, exit_code, NONE_SILENT_PRINT_INTRO + prints
    mock_install_commands_if_missing.assert_called_once_with(
        [
            COMMAND_INSTANCE1,
            COMMAND_INSTANCE2,
            COMMAND_INSTANCE3,
            COMMAND_INSTANCE4,
            COMMAND_INSTANCE5,
        ],
        verbosity=DEFAULT_VERBOSITY,
    )
    mock_read_commands_map.assert_called_with(
        (), contexts=(), allow_list=(), deny_list=()
    )
    mock_evaluate_commands_map.assert_called_with(
        commands_map=COMMANDS_MAP, print_method=click.echo, verbosity=DEFAULT_VERBOSITY
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
