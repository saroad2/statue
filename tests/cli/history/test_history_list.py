import datetime
import uuid

from pytest_cases import THIS_MODULE, parametrize_with_cases

from statue.cli import statue_cli
from tests.util import evaluation_mock


def case_empty_history():
    additional_flags = []
    evaluations = []
    output = "No previous evaluations.\n"
    return additional_flags, evaluations, output


def case_one_successful_evaluation():
    total_commands = 4
    timestamp1 = datetime.datetime(
        year=2020, month=4, day=15, hour=12, minute=7, second=42
    )

    additional_flags = []
    evaluations = [
        evaluation_mock(
            timestamp=timestamp1,
            successful_commands=total_commands,
            total_commands=total_commands,
            total_execution_duration=0.234,
        )
    ]
    output = "1) 04/15/2020, 12:07:42 - Success (4/4 successful, 0.23 seconds)\n"
    return additional_flags, evaluations, output


def case_one_failed_evaluation():
    additional_flags = []
    timestamp1 = datetime.datetime(
        year=2020, month=5, day=12, hour=14, minute=8, second=23
    )
    evaluations = [
        evaluation_mock(
            timestamp=timestamp1,
            successful_commands=3,
            total_commands=4,
            total_execution_duration=0.591,
        )
    ]
    output = "1) 05/12/2020, 14:08:23 - Failure (3/4 successful, 0.59 seconds)\n"
    return additional_flags, evaluations, output


def case_two_successful_evaluations():
    total_commands1, total_commands2 = 4, 7

    additional_flags = []
    timestamp1, timestamp2 = (
        datetime.datetime(year=2020, month=4, day=15, hour=12, minute=7, second=42),
        datetime.datetime(year=2020, month=4, day=14, hour=18, minute=59, second=11),
    )
    evaluations = [
        evaluation_mock(
            timestamp=timestamp1,
            successful_commands=total_commands1,
            total_commands=total_commands1,
            total_execution_duration=0.234,
        ),
        evaluation_mock(
            timestamp=timestamp2,
            successful_commands=total_commands2,
            total_commands=total_commands2,
            total_execution_duration=0.189,
        ),
    ]
    output = (
        "1) 04/15/2020, 12:07:42 - Success (4/4 successful, 0.23 seconds)\n"
        "2) 04/14/2020, 18:59:11 - Success (7/7 successful, 0.19 seconds)\n"
    )
    return additional_flags, evaluations, output


def case_one_failed_and_one_successful():
    total_commands = 4

    additional_flags = []
    timestamp1, timestamp2 = (
        datetime.datetime(year=2020, month=4, day=15, hour=12, minute=7, second=42),
        datetime.datetime(year=2020, month=4, day=14, hour=18, minute=59, second=11),
    )
    evaluations = [
        evaluation_mock(
            timestamp=timestamp1,
            successful_commands=total_commands,
            total_commands=total_commands,
            total_execution_duration=0.234,
        ),
        evaluation_mock(
            timestamp=timestamp2,
            successful_commands=3,
            total_commands=7,
            total_execution_duration=0.189,
        ),
    ]
    output = (
        "1) 04/15/2020, 12:07:42 - Success (4/4 successful, 0.23 seconds)\n"
        "2) 04/14/2020, 18:59:11 - Failure (3/7 successful, 0.19 seconds)\n"
    )
    return additional_flags, evaluations, output


def case_three_evaluations():
    total_commands1, total_commands2 = 4, 10

    additional_flags = []
    timestamp1, timestamp2, timestamp3 = (
        datetime.datetime(year=2020, month=4, day=15, hour=12, minute=7, second=42),
        datetime.datetime(year=2020, month=4, day=14, hour=18, minute=59, second=11),
        datetime.datetime(year=2020, month=4, day=14, hour=11, minute=31, second=22),
    )
    evaluations = [
        evaluation_mock(
            timestamp=timestamp1,
            successful_commands=total_commands1,
            total_commands=total_commands1,
            total_execution_duration=0.234,
        ),
        evaluation_mock(
            timestamp=timestamp2,
            successful_commands=3,
            total_commands=7,
            total_execution_duration=0.189,
        ),
        evaluation_mock(
            timestamp=timestamp3,
            successful_commands=total_commands2,
            total_commands=total_commands2,
            total_execution_duration=0.03,
        ),
    ]
    output = (
        "1) 04/15/2020, 12:07:42 - Success (4/4 successful, 0.23 seconds)\n"
        "2) 04/14/2020, 18:59:11 - Failure (3/7 successful, 0.19 seconds)\n"
        "3) 04/14/2020, 11:31:22 - Success (10/10 successful, 0.03 seconds)\n"
    )
    return additional_flags, evaluations, output


def case_head_flag():
    total_commands1, total_commands2 = 4, 10

    additional_flags = ["--head=2"]
    timestamp1, timestamp2, timestamp3 = (
        datetime.datetime(year=2020, month=4, day=15, hour=12, minute=7, second=42),
        datetime.datetime(year=2020, month=4, day=14, hour=18, minute=59, second=11),
        datetime.datetime(year=2020, month=4, day=14, hour=11, minute=31, second=22),
    )
    evaluations = [
        evaluation_mock(
            timestamp=timestamp1,
            successful_commands=total_commands1,
            total_commands=total_commands1,
            total_execution_duration=0.234,
        ),
        evaluation_mock(
            timestamp=timestamp2,
            successful_commands=3,
            total_commands=7,
            total_execution_duration=0.189,
        ),
        evaluation_mock(
            timestamp=timestamp3,
            successful_commands=total_commands2,
            total_commands=total_commands2,
            total_execution_duration=0.03,
        ),
    ]
    output = (
        "1) 04/15/2020, 12:07:42 - Success (4/4 successful, 0.23 seconds)\n"
        "2) 04/14/2020, 18:59:11 - Failure (3/7 successful, 0.19 seconds)\n"
    )
    return additional_flags, evaluations, output


@parametrize_with_cases(
    argnames=["additional_flags", "evaluations", "output"],
    cases=THIS_MODULE,
)
def test_history_list(
    additional_flags,
    evaluations,
    output,
    cli_runner,
    mock_evaluation_load_from_file,
    mock_build_configuration_from_file,
):
    configuration = mock_build_configuration_from_file.return_value
    configuration.cache.all_evaluation_paths = [
        f"evaluation_{uuid.uuid4()}.json" for _ in range(len(evaluations))
    ]
    mock_evaluation_load_from_file.side_effect = evaluations

    result = cli_runner.invoke(statue_cli, ["history", "list", *additional_flags])

    assert (
        result.exit_code == 0
    ), f"Execution failed with the following error: '{result.exception}'"
    assert result.output == output
