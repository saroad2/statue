import datetime

import regex

from statue.cli.cli import statue as statue_cli
from tests.util import evaluation_mock

EPOCH = datetime.datetime.utcfromtimestamp(0)
TIME_REGEX = r"\d\d/\d\d/\d\d\d\d, \d\d:\d\d:\d\d"


def assert_evaluations(result, evaluations):
    assert (
        result.exit_code == 0
    ), f"History list existed with no 0 return code. Got exception {result.exception}"
    for i, evaluation in enumerate(evaluations, start=1):
        successful = "Success" if evaluation.success else "Failure"
        success_ratio = (
            rf"\({evaluation.successful_commands_number}/{evaluation.commands_number} "
            r"successful\)"
        )
        assert regex.search(
            fr"{i}\) {TIME_REGEX} - {successful} {success_ratio}", result.output
        )


def test_history_empty_list(cli_runner, mock_cwd):

    result = cli_runner.invoke(statue_cli, ["history", "list"])

    assert result.exit_code == 0
    assert result.output == "No previous evaluations.\n"


def test_history_list_not_empty(cli_runner, mock_cwd, mock_evaluation_load_from_file):
    times = (
        datetime.datetime(year=2021, month=10, day=28, hour=16, minute=38, second=15),
        datetime.datetime(year=2021, month=10, day=28, hour=12, minute=17, second=59),
        datetime.datetime(year=2021, month=10, day=27, hour=19, minute=20, second=0),
    )
    times_seconds_since_epoch = [
        int((time_stamp - EPOCH).total_seconds()) for time_stamp in times
    ]
    evaluations_dir = mock_cwd / ".statue" / "evaluations"
    evaluations_dir.mkdir(parents=True)
    for seconds in times_seconds_since_epoch:
        (evaluations_dir / f"evaluation-{seconds}.json").touch()
    evaluations = [
        evaluation_mock(successful_commands=10, total_commands=10),
        evaluation_mock(successful_commands=2, total_commands=3),
        evaluation_mock(successful_commands=7, total_commands=7),
    ]
    mock_evaluation_load_from_file.side_effect = evaluations

    result = cli_runner.invoke(statue_cli, ["history", "list"])

    assert_evaluations(result, evaluations)


def test_history_list_with_head(cli_runner, mock_cwd, mock_evaluation_load_from_file):
    times = (
        datetime.datetime(year=2021, month=10, day=28, hour=16, minute=38, second=15),
        datetime.datetime(year=2021, month=10, day=28, hour=12, minute=17, second=59),
        datetime.datetime(year=2021, month=10, day=27, hour=19, minute=20, second=0),
        datetime.datetime(year=2020, month=12, day=1, hour=10, minute=15, second=35),
    )
    times_seconds_since_epoch = [
        int((time_stamp - EPOCH).total_seconds()) for time_stamp in times
    ]
    evaluations_dir = mock_cwd / ".statue" / "evaluations"
    evaluations_dir.mkdir(parents=True)
    for seconds in times_seconds_since_epoch:
        (evaluations_dir / f"evaluation-{seconds}.json").touch()
    evaluations = [
        evaluation_mock(successful_commands=2, total_commands=3),
        evaluation_mock(successful_commands=10, total_commands=12),
        evaluation_mock(successful_commands=3, total_commands=3),
    ]
    mock_evaluation_load_from_file.side_effect = evaluations

    result = cli_runner.invoke(statue_cli, ["history", "list", "--head", "3"])

    assert_evaluations(result, evaluations)
