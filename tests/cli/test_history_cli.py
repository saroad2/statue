import datetime
from unittest import mock

import regex

from statue.cli.cli import statue_cli
from statue.evaluation import CommandEvaluation, Evaluation, SourceEvaluation
from tests.constants import (
    COMMAND1,
    COMMAND2,
    COMMAND3,
    COMMAND4,
    COMMAND5,
    SOURCE1,
    SOURCE2,
)
from tests.util import command_mock, evaluation_mock

EPOCH = datetime.datetime.utcfromtimestamp(0)
TIME_REGEX = r"\d\d/\d\d/\d\d\d\d, \d\d:\d\d:\d\d"
EVALUATION = Evaluation(
    {
        SOURCE1: SourceEvaluation(
            [
                CommandEvaluation(command=command_mock(name=COMMAND1), success=True),
                CommandEvaluation(command=command_mock(name=COMMAND2), success=False),
                CommandEvaluation(command=command_mock(name=COMMAND3), success=True),
            ]
        ),
        SOURCE2: SourceEvaluation(
            [
                CommandEvaluation(command=command_mock(name=COMMAND4), success=True),
                CommandEvaluation(command=command_mock(name=COMMAND5), success=False),
            ]
        ),
    }
)
EVALUATION_REPORT = f"""{SOURCE1}:
\t{COMMAND1} - Success
\t{COMMAND2} - Failure
\t{COMMAND3} - Success
{SOURCE2}:
\t{COMMAND4} - Success
\t{COMMAND5} - Failure
"""


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


def test_show_recent_evaluation(
    cli_runner, mock_cache_evaluation_path, mock_evaluation_load_from_file
):
    mock_evaluation_load_from_file.return_value = EVALUATION

    result = cli_runner.invoke(statue_cli, ["history", "show"])

    assert result.exit_code == 0
    assert EVALUATION_REPORT in result.output
    mock_cache_evaluation_path.assert_called_once_with(0)
    mock_evaluation_load_from_file.assert_called_once_with(
        mock_cache_evaluation_path.return_value
    )


def test_show_recent_evaluation_explicitly(
    cli_runner, mock_cache_evaluation_path, mock_evaluation_load_from_file
):
    mock_evaluation_load_from_file.return_value = EVALUATION

    result = cli_runner.invoke(statue_cli, ["history", "show", "-n", "1"])

    assert result.exit_code == 0
    assert EVALUATION_REPORT in result.output
    mock_cache_evaluation_path.assert_called_once_with(0)
    mock_evaluation_load_from_file.assert_called_once_with(
        mock_cache_evaluation_path.return_value
    )


def test_show_3rd_recent_evaluation_explicitly(
    cli_runner, mock_cache_evaluation_path, mock_evaluation_load_from_file
):
    mock_evaluation_load_from_file.return_value = EVALUATION

    result = cli_runner.invoke(statue_cli, ["history", "show", "-n", "3"])

    assert result.exit_code == 0
    assert EVALUATION_REPORT in result.output
    mock_cache_evaluation_path.assert_called_once_with(2)
    mock_evaluation_load_from_file.assert_called_once_with(
        mock_cache_evaluation_path.return_value
    )


def test_show_with_number_zero(
    cli_runner, mock_cache_evaluation_path, mock_evaluation_load_from_file
):

    result = cli_runner.invoke(statue_cli, ["history", "show", "-n", "0"])

    assert result.exit_code == 2
    assert "Number should be 1 or greater. got 0" in result.output


def test_show_with_negative_number(
    cli_runner, mock_cache_evaluation_path, mock_evaluation_load_from_file
):

    result = cli_runner.invoke(statue_cli, ["history", "show", "-n", "-2"])

    assert result.exit_code == 2
    assert "Number should be 1 or greater. got -2" in result.output


def test_clear_empty_history(cli_runner, mock_cache_all_evaluation_paths):
    mock_cache_all_evaluation_paths.return_value = []

    result = cli_runner.invoke(statue_cli, ["history", "clear"])

    assert (
        result.exit_code == 0
    ), f"Exited with non successful exit code. {result.exception}"
    assert "No previous evaluations." in result.output


def test_clear_all_history_approved(cli_runner, mock_cache_all_evaluation_paths):
    history_size = 40
    evaluation_files = [mock.Mock() for _ in range(history_size)]
    mock_cache_all_evaluation_paths.return_value = evaluation_files

    result = cli_runner.invoke(statue_cli, ["history", "clear"], input="y")

    assert (
        result.exit_code == 0
    ), f"Exited with non successful exit code. {result.exception}"
    for evaluation_file in evaluation_files:
        evaluation_file.unlink.assert_called_once_with()


def test_clear_all_history_denied(cli_runner, mock_cache_all_evaluation_paths):
    history_size = 40
    evaluation_files = [mock.Mock() for _ in range(history_size)]
    mock_cache_all_evaluation_paths.return_value = evaluation_files

    result = cli_runner.invoke(statue_cli, ["history", "clear"], input="n")

    assert (
        result.exit_code == 0
    ), f"Exited with non successful exit code. {result.exception}"
    for evaluation_file in evaluation_files:
        evaluation_file.unlink.assert_not_called()


def test_clear_all_history_forced(cli_runner, mock_cache_all_evaluation_paths):
    history_size = 40
    evaluation_files = [mock.Mock() for _ in range(history_size)]
    mock_cache_all_evaluation_paths.return_value = evaluation_files

    result = cli_runner.invoke(statue_cli, ["history", "clear", "-f"])

    assert (
        result.exit_code == 0
    ), f"Exited with non successful exit code. {result.exception}"
    for evaluation_file in evaluation_files:
        evaluation_file.unlink.assert_called_once_with()


def test_clear_all_history_limited(cli_runner, mock_cache_all_evaluation_paths):
    history_size = 40
    limit = 15
    evaluation_files = [mock.Mock() for _ in range(history_size)]
    mock_cache_all_evaluation_paths.return_value = evaluation_files

    result = cli_runner.invoke(
        statue_cli, ["history", "clear", "-l", str(limit)], input="y"
    )

    assert (
        result.exit_code == 0
    ), f"Exited with non successful exit code. {result.exception}"
    for evaluation_file in evaluation_files[:-limit]:
        evaluation_file.unlink.assert_not_called()
    for evaluation_file in evaluation_files[-limit:]:
        evaluation_file.unlink.assert_called_once_with()


def test_clear_all_history_limited_with_high_limit(
    cli_runner, mock_cache_all_evaluation_paths
):
    history_size = 40
    limit = 70
    evaluation_files = [mock.Mock() for _ in range(history_size)]
    mock_cache_all_evaluation_paths.return_value = evaluation_files

    result = cli_runner.invoke(
        statue_cli, ["history", "clear", "-l", str(limit)], input="y"
    )

    assert (
        result.exit_code == 0
    ), f"Exited with non successful exit code. {result.exception}"
    for evaluation_file in evaluation_files:
        evaluation_file.unlink.assert_called_once_with()
