import random

import pytest

from statue.cli import statue_cli


def test_history_clear_empty_history(cli_runner, mock_build_configuration_from_file):
    configuration = mock_build_configuration_from_file.return_value
    configuration.cache.number_of_evaluations = 0

    result = cli_runner.invoke(statue_cli, ["history", "clear"])

    assert result.exit_code == 0
    assert result.output == "No previous evaluations.\n"


def test_history_clear_confirmed(
    cli_runner,
    mock_build_configuration_from_file,
):
    number_of_evaluations = random.randint(1, 5)

    configuration = mock_build_configuration_from_file.return_value
    configuration.cache.number_of_evaluations = number_of_evaluations

    result = cli_runner.invoke(statue_cli, ["history", "clear"], input="y")

    assert result.exit_code == 0
    assert result.output == (
        f"{number_of_evaluations} evaluation files are about to be deleted. "
        "Are you sure you want to delete them? [y/N]: y\n"
        f"{number_of_evaluations} evaluation files have been deleted successfully.\n"
    )
    configuration.cache.clear.assert_called_once_with(limit=None)


def test_history_clear_not_confirmed(
    cli_runner,
    mock_build_configuration_from_file,
):
    number_of_evaluations = random.randint(1, 5)

    configuration = mock_build_configuration_from_file.return_value
    configuration.cache.number_of_evaluations = number_of_evaluations

    result = cli_runner.invoke(statue_cli, ["history", "clear"], input="n")

    assert result.exit_code == 0
    assert result.output == (
        f"{number_of_evaluations} evaluation files are about to be deleted. "
        "Are you sure you want to delete them? [y/N]: n\n"
        "Aborted without clearing history.\n"
    )
    configuration.cache.clear.assert_not_called()


@pytest.mark.parametrize(argnames=["force_flag"], argvalues=[("-f",), ("--force",)])
def test_history_clear_forced(
    force_flag,
    cli_runner,
    mock_build_configuration_from_file,
):
    number_of_evaluations = random.randint(1, 5)

    configuration = mock_build_configuration_from_file.return_value
    configuration.cache.number_of_evaluations = number_of_evaluations

    result = cli_runner.invoke(statue_cli, ["history", "clear", force_flag])

    assert result.exit_code == 0
    assert result.output == (
        f"{number_of_evaluations} evaluation files have been deleted successfully.\n"
    )
    configuration.cache.clear.assert_called_once_with(limit=None)


@pytest.mark.parametrize(argnames=["limit_flag"], argvalues=[("-l",), ("--limit",)])
def test_history_clear_limited(
    limit_flag,
    cli_runner,
    mock_build_configuration_from_file,
):
    limited_number = 3
    number_of_evaluations = limited_number + random.randint(1, 5)

    configuration = mock_build_configuration_from_file.return_value
    configuration.cache.number_of_evaluations = number_of_evaluations

    result = cli_runner.invoke(
        statue_cli, ["history", "clear", limit_flag, limited_number], input="y"
    )

    assert result.exit_code == 0
    assert result.output == (
        f"{limited_number} evaluation files are about to be deleted. "
        "Are you sure you want to delete them? [y/N]: y\n"
        f"{limited_number} evaluation files have been deleted successfully.\n"
    )
    configuration.cache.clear.assert_called_once_with(limit=limited_number)
