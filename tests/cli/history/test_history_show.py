import datetime

from pytest_cases import THIS_MODULE, parametrize_with_cases

from statue.cli import statue_cli
from statue.command import CommandEvaluation
from statue.evaluation import Evaluation, SourceEvaluation
from statue.exceptions import CacheError
from tests.constants import ARG1, ARG2, ARG3, ARG4, COMMAND1, COMMAND2, SOURCE1, SOURCE2
from tests.util import command_mock


def case_empty_evaluation():
    timestamp = datetime.datetime(
        year=2020, month=4, day=15, hour=12, minute=7, second=42
    )
    return dict(
        additional_flags=[],
        evaluation_number=0,
        evaluation=Evaluation(timestamp=timestamp),
        output="04/15/2020, 12:07:42 - Success (0/0 successful, 0.00 seconds)\n",
    )


def case_one_source_one_command():
    timestamp = datetime.datetime(
        year=2020, month=4, day=15, hour=12, minute=7, second=42
    )
    return dict(
        additional_flags=[],
        evaluation_number=0,
        evaluation=Evaluation(
            timestamp=timestamp,
            total_execution_duration=18.1,
            sources_evaluations={
                SOURCE1: SourceEvaluation(
                    commands_evaluations=[
                        CommandEvaluation(
                            command=command_mock(COMMAND1),
                            success=True,
                            execution_duration=0.67,
                        )
                    ],
                    source_execution_duration=1.199,
                )
            },
        ),
        output=(
            "04/15/2020, 12:07:42 - Success (1/1 successful, 18.10 seconds)\n"
            f"{SOURCE1} (1.20 seconds):\n"
            f"\t{COMMAND1} - Success (0.67 seconds)\n"
        ),
    )


def case_one_source_two_commands_success():
    timestamp = datetime.datetime(
        year=2020, month=4, day=15, hour=12, minute=7, second=42
    )
    return dict(
        additional_flags=[],
        evaluation_number=0,
        evaluation=Evaluation(
            timestamp=timestamp,
            total_execution_duration=18.1,
            sources_evaluations={
                SOURCE1: SourceEvaluation(
                    commands_evaluations=[
                        CommandEvaluation(
                            command=command_mock(COMMAND1),
                            success=True,
                            execution_duration=0.67,
                        ),
                        CommandEvaluation(
                            command=command_mock(COMMAND2),
                            success=True,
                            execution_duration=1.632,
                        ),
                    ],
                    source_execution_duration=1.199,
                )
            },
        ),
        output=(
            "04/15/2020, 12:07:42 - Success (2/2 successful, 18.10 seconds)\n"
            f"{SOURCE1} (1.20 seconds):\n"
            f"\t{COMMAND1} - Success (0.67 seconds)\n"
            f"\t{COMMAND2} - Success (1.63 seconds)\n"
        ),
    )


def case_one_source_two_commands_success_verbosely():
    timestamp = datetime.datetime(
        year=2020, month=4, day=15, hour=12, minute=7, second=42
    )
    return dict(
        additional_flags=["--verbose"],
        evaluation_number=0,
        evaluation=Evaluation(
            timestamp=timestamp,
            total_execution_duration=18.1,
            sources_evaluations={
                SOURCE1: SourceEvaluation(
                    commands_evaluations=[
                        CommandEvaluation(
                            command=command_mock(COMMAND1, args=[ARG1, ARG2]),
                            success=True,
                            execution_duration=0.67,
                        ),
                        CommandEvaluation(
                            command=command_mock(COMMAND2, args=[ARG3, ARG4]),
                            success=True,
                            execution_duration=1.632,
                        ),
                    ],
                    source_execution_duration=1.199,
                )
            },
        ),
        output=(
            "04/15/2020, 12:07:42 - Success (2/2 successful, 18.10 seconds)\n"
            f"{SOURCE1} (1.20 seconds):\n"
            f"\t{COMMAND1} - Success (0.67 seconds)\n"
            f"\t\tArguments: {ARG1} {ARG2}\n"
            f"\t{COMMAND2} - Success (1.63 seconds)\n"
            f"\t\tArguments: {ARG3} {ARG4}\n"
        ),
    )


def case_one_source_two_commands_failure():
    timestamp = datetime.datetime(
        year=2020, month=4, day=15, hour=12, minute=7, second=42
    )
    return dict(
        additional_flags=[],
        evaluation_number=0,
        evaluation=Evaluation(
            timestamp=timestamp,
            total_execution_duration=18.1,
            sources_evaluations={
                SOURCE1: SourceEvaluation(
                    commands_evaluations=[
                        CommandEvaluation(
                            command=command_mock(COMMAND1),
                            success=True,
                            execution_duration=0.67,
                        ),
                        CommandEvaluation(
                            command=command_mock(COMMAND2),
                            success=False,
                            execution_duration=1.632,
                        ),
                    ],
                    source_execution_duration=1.199,
                )
            },
        ),
        output=(
            "04/15/2020, 12:07:42 - Failure (1/2 successful, 18.10 seconds)\n"
            f"{SOURCE1} (1.20 seconds):\n"
            f"\t{COMMAND1} - Success (0.67 seconds)\n"
            f"\t{COMMAND2} - Failure (1.63 seconds)\n"
        ),
    )


def case_two_sources_two_commands():
    timestamp = datetime.datetime(
        year=2020, month=4, day=15, hour=12, minute=7, second=42
    )
    return dict(
        additional_flags=[],
        evaluation_number=0,
        evaluation=Evaluation(
            timestamp=timestamp,
            total_execution_duration=18.1,
            sources_evaluations={
                SOURCE1: SourceEvaluation(
                    commands_evaluations=[
                        CommandEvaluation(
                            command=command_mock(COMMAND1),
                            success=True,
                            execution_duration=0.67,
                        )
                    ],
                    source_execution_duration=1.199,
                ),
                SOURCE2: SourceEvaluation(
                    commands_evaluations=[
                        CommandEvaluation(
                            command=command_mock(COMMAND2),
                            success=False,
                            execution_duration=1.632,
                        )
                    ],
                    source_execution_duration=2.89,
                ),
            },
        ),
        output=(
            "04/15/2020, 12:07:42 - Failure (1/2 successful, 18.10 seconds)\n"
            f"{SOURCE1} (1.20 seconds):\n"
            f"\t{COMMAND1} - Success (0.67 seconds)\n"
            f"{SOURCE2} (2.89 seconds):\n"
            f"\t{COMMAND2} - Failure (1.63 seconds)\n"
        ),
    )


def case_number_flag():
    timestamp = datetime.datetime(
        year=2020, month=4, day=15, hour=12, minute=7, second=42
    )
    return dict(
        additional_flags=["-n", "5"],
        evaluation_number=4,
        evaluation=Evaluation(timestamp=timestamp),
        output="04/15/2020, 12:07:42 - Success (0/0 successful, 0.00 seconds)\n",
    )


@parametrize_with_cases(argnames="case", cases=THIS_MODULE, prefix="case_")
def test_history_show(
    case,
    cli_runner,
    mock_evaluation_load_from_file,
    mock_build_configuration_from_file,
):
    evaluation = case["evaluation"]
    configuration = mock_build_configuration_from_file.return_value
    configuration.cache.get_evaluation.return_value = evaluation

    result = cli_runner.invoke(
        statue_cli, ["history", "show", *case["additional_flags"]]
    )

    assert (
        result.exit_code == 0
    ), f"Execution failed with the following error: '{result.exception}'"
    configuration.cache.get_evaluation.assert_called_once_with(
        case["evaluation_number"]
    )
    assert result.output == case["output"]


def test_history_show_fail_on_invalid_index(
    cli_runner, mock_build_configuration_from_file
):
    configuration = mock_build_configuration_from_file.return_value
    configuration.cache.get_evaluation.side_effect = CacheError
    result = cli_runner.invoke(statue_cli, ["history", "show", "-n", "-6"])

    assert result.exit_code == 1
    assert result.output == "Could not find evaluation with given index -6\n"
