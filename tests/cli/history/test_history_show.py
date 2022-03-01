import datetime
import uuid

from pytest_cases import THIS_MODULE, parametrize_with_cases

from statue.cli import statue_cli
from statue.command import CommandEvaluation
from statue.evaluation import Evaluation, SourceEvaluation
from tests.constants import COMMAND1, COMMAND2, SOURCE1, SOURCE2
from tests.util import command_mock


def case_empty_evaluation():
    return dict(
        additional_flags=[],
        evaluation_number=0,
        evaluation=Evaluation(),
        datetime=datetime.datetime(
            year=2020, month=4, day=15, hour=12, minute=7, second=42
        ),
        output="04/15/2020, 12:07:42 - Success (0/0 successful, 0.00 seconds)\n",
    )


def case_one_source_one_command():
    return dict(
        additional_flags=[],
        evaluation_number=0,
        evaluation=Evaluation(
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
        datetime=datetime.datetime(
            year=2020, month=4, day=15, hour=12, minute=7, second=42
        ),
        output=(
            "04/15/2020, 12:07:42 - Success (1/1 successful, 18.10 seconds)\n"
            f"{SOURCE1} (1.20 seconds):\n"
            f"\t{COMMAND1} - Success (0.67 seconds)\n"
        ),
    )


def case_one_source_two_commands_success():
    return dict(
        additional_flags=[],
        evaluation_number=0,
        evaluation=Evaluation(
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
        datetime=datetime.datetime(
            year=2020, month=4, day=15, hour=12, minute=7, second=42
        ),
        output=(
            "04/15/2020, 12:07:42 - Success (2/2 successful, 18.10 seconds)\n"
            f"{SOURCE1} (1.20 seconds):\n"
            f"\t{COMMAND1} - Success (0.67 seconds)\n"
            f"\t{COMMAND2} - Success (1.63 seconds)\n"
        ),
    )


def case_one_source_two_commands_failure():
    return dict(
        additional_flags=[],
        evaluation_number=0,
        evaluation=Evaluation(
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
        datetime=datetime.datetime(
            year=2020, month=4, day=15, hour=12, minute=7, second=42
        ),
        output=(
            "04/15/2020, 12:07:42 - Failure (1/2 successful, 18.10 seconds)\n"
            f"{SOURCE1} (1.20 seconds):\n"
            f"\t{COMMAND1} - Success (0.67 seconds)\n"
            f"\t{COMMAND2} - Failure (1.63 seconds)\n"
        ),
    )


def case_two_sources_two_commands():
    return dict(
        additional_flags=[],
        evaluation_number=0,
        evaluation=Evaluation(
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
        datetime=datetime.datetime(
            year=2020, month=4, day=15, hour=12, minute=7, second=42
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
    return dict(
        additional_flags=["-n", "5"],
        evaluation_number=4,
        evaluation=Evaluation(),
        datetime=datetime.datetime(
            year=2020, month=4, day=15, hour=12, minute=7, second=42
        ),
        output="04/15/2020, 12:07:42 - Success (0/0 successful, 0.00 seconds)\n",
    )


@parametrize_with_cases(argnames="case", cases=THIS_MODULE, prefix="case_")
def test_history_show(
    case,
    cli_runner,
    clear_configuration,
    mock_cache_evaluation_path,
    mock_evaluation_load_from_file,
    mock_cache_extract_time_stamp_from_path,
    mock_load_from_configuration_file,
):
    evaluation_path = f"evaluation_{uuid.uuid4()}.json"
    mock_cache_evaluation_path.return_value = evaluation_path
    mock_evaluation_load_from_file.return_value = case["evaluation"]
    mock_cache_extract_time_stamp_from_path.return_value = case["datetime"].timestamp()

    result = cli_runner.invoke(
        statue_cli, ["history", "show", *case["additional_flags"]]
    )

    assert (
        result.exit_code == 0
    ), f"Execution failed with the following error: '{result.exception}'"
    mock_cache_evaluation_path.assert_called_once_with(case["evaluation_number"])
    mock_evaluation_load_from_file.assert_called_once_with(evaluation_path)
    mock_cache_extract_time_stamp_from_path.assert_called_once_with(evaluation_path)
    assert result.output == case["output"]


def test_history_show_fail_on_negative_number(cli_runner):

    result = cli_runner.invoke(statue_cli, ["history", "show", "-n", "-6"])

    assert result.exit_code == 2
    assert "Number should be 1 or greater. got -6" in result.output
