import random
from unittest import mock

import pytest

from statue.cli import statue_cli


def test_history_clear_empty_history(cli_runner, mock_cache_all_evaluation_paths):
    mock_cache_all_evaluation_paths.return_value = []

    result = cli_runner.invoke(statue_cli, ["history", "clear"])

    assert result.exit_code == 0
    assert result.output == "No previous evaluations.\n"


def test_history_clear_confirmed(cli_runner, mock_cache_all_evaluation_paths):
    number_of_evaluations = random.randint(1, 5)
    evaluation_paths = [mock.Mock() for _ in range(number_of_evaluations)]
    mock_cache_all_evaluation_paths.return_value = evaluation_paths

    result = cli_runner.invoke(statue_cli, ["history", "clear"], input="y")

    assert result.exit_code == 0
    assert result.output == (
        f"{number_of_evaluations} evaluation files are about to be deleted. "
        "Are you wish to delete those? [y/N]: y\n"
        f"{number_of_evaluations} evaluation files have been deleted successfully.\n"
    )

    for evaluation_path in evaluation_paths:
        evaluation_path.unlink.assert_called_once_with()


def test_history_clear_not_confirmed(cli_runner, mock_cache_all_evaluation_paths):
    number_of_evaluations = random.randint(1, 5)
    evaluation_paths = [mock.Mock() for _ in range(number_of_evaluations)]
    mock_cache_all_evaluation_paths.return_value = evaluation_paths

    result = cli_runner.invoke(statue_cli, ["history", "clear"], input="n")

    assert result.exit_code == 0
    assert result.output == (
        f"{number_of_evaluations} evaluation files are about to be deleted. "
        "Are you wish to delete those? [y/N]: n\n"
        "Aborted without clearing history.\n"
    )

    for evaluation_path in evaluation_paths:
        evaluation_path.unlink.assert_not_called()


@pytest.mark.parametrize(argnames=["force_flag"], argvalues=[("-f",), ("--force",)])
def test_history_clear_forced(force_flag, cli_runner, mock_cache_all_evaluation_paths):
    number_of_evaluations = random.randint(1, 5)
    evaluation_paths = [mock.Mock() for _ in range(number_of_evaluations)]
    mock_cache_all_evaluation_paths.return_value = evaluation_paths

    result = cli_runner.invoke(statue_cli, ["history", "clear", force_flag])

    assert result.exit_code == 0
    assert result.output == (
        f"{number_of_evaluations} evaluation files have been deleted successfully.\n"
    )

    for evaluation_path in evaluation_paths:
        evaluation_path.unlink.assert_called_once_with()


@pytest.mark.parametrize(argnames=["limit_flag"], argvalues=[("-l",), ("--limit",)])
def test_history_clear_limited(limit_flag, cli_runner, mock_cache_all_evaluation_paths):
    limited_number = 3
    number_of_evaluations = limited_number + random.randint(1, 5)
    evaluation_paths = [mock.Mock() for _ in range(number_of_evaluations)]
    mock_cache_all_evaluation_paths.return_value = evaluation_paths

    result = cli_runner.invoke(
        statue_cli, ["history", "clear", limit_flag, limited_number], input="y"
    )

    assert result.exit_code == 0
    assert result.output == (
        f"{limited_number} evaluation files are about to be deleted. "
        "Are you wish to delete those? [y/N]: y\n"
        f"{limited_number} evaluation files have been deleted successfully.\n"
    )

    for evaluation_path in evaluation_paths[:-limited_number]:
        evaluation_path.unlink.assert_not_called()
    for evaluation_path in evaluation_paths[-limited_number:]:
        evaluation_path.unlink.assert_called_once_with()
