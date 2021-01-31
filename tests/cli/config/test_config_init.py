from pathlib import Path
from unittest import mock

from git import InvalidGitRepositoryError
from pytest_cases import THIS_MODULE, parametrize_with_cases

from statue.cli.cli import statue_cli as statue_cli
from statue.constants import CONTEXTS, SOURCES, STANDARD


def case_empty_sources():
    return [], {SOURCES: {}}


def case_regular_sources():
    src = "src"
    return [src], {SOURCES: {src: {CONTEXTS: [STANDARD]}}}


def case_internal_path():
    """Paths should always be written as posix paths, even in windows"""
    return [Path("src", "package")], {SOURCES: {"src/package": {CONTEXTS: [STANDARD]}}}


def case_test_sources():
    test = "test"
    return [test], {SOURCES: {test: {CONTEXTS: ["test"]}}}


def case_setup_sources():
    setup = "setup.py"
    return [setup], {SOURCES: {setup: {CONTEXTS: ["fast"]}}}


def case_all_sources():
    return ["src", "test", "setup.py"], {
        SOURCES: {
            "src": {CONTEXTS: [STANDARD]},
            "test": {CONTEXTS: ["test"]},
            "setup.py": {CONTEXTS: ["fast"]},
        }
    }


@parametrize_with_cases(argnames="sources, expected_config", cases=THIS_MODULE)
def test_config_init(
    sources,
    expected_config,
    mock_load_configuration,
    mock_configuration_path,
    mock_cwd,
    mock_find_sources,
    mock_toml_dump,
    mock_git_repo,
    cli_runner,
):
    mock_find_sources.return_value = [mock_cwd / source for source in sources]
    mock_open = mock.mock_open()
    with mock.patch("statue.cli.config.open", mock_open):
        result = cli_runner.invoke(statue_cli, ["config", "init"])
        mock_open.assert_called_once_with(
            mock_configuration_path.return_value, mode="w"
        )
        mock_toml_dump.assert_called_once_with(expected_config, mock_open.return_value)
    mock_find_sources.assert_called_once_with(mock_cwd, repo=mock_git_repo.return_value)
    assert result.exit_code == 0


@parametrize_with_cases(argnames="sources, expected_config", cases=THIS_MODULE)
def test_config_init_without_repo(
    sources,
    expected_config,
    mock_load_configuration,
    mock_configuration_path,
    mock_cwd,
    mock_find_sources,
    mock_toml_dump,
    mock_git_repo,
    cli_runner,
):
    mock_git_repo.side_effect = InvalidGitRepositoryError()
    mock_find_sources.return_value = [mock_cwd / source for source in sources]
    mock_open = mock.mock_open()
    with mock.patch("statue.cli.config.open", mock_open):
        result = cli_runner.invoke(statue_cli, ["config", "init"])
        mock_open.assert_called_once_with(
            mock_configuration_path.return_value, mode="w"
        )
        mock_toml_dump.assert_called_once_with(expected_config, mock_open.return_value)
    mock_find_sources.assert_called_once_with(mock_cwd, repo=None)
    assert result.exit_code == 0


@parametrize_with_cases(argnames="sources, expected_config", cases=THIS_MODULE)
def test_config_init_with_directory(
    sources,
    expected_config,
    mock_load_configuration,
    mock_configuration_path,
    tmp_path,
    mock_find_sources,
    mock_toml_dump,
    mock_git_repo,
    cli_runner,
):
    mock_find_sources.return_value = [tmp_path / source for source in sources]
    mock_open = mock.mock_open()
    with mock.patch("statue.cli.config.open", mock_open):
        result = cli_runner.invoke(statue_cli, ["config", "init", "-d", str(tmp_path)])
        mock_open.assert_called_once_with(
            mock_configuration_path.return_value, mode="w"
        )
        mock_toml_dump.assert_called_once_with(expected_config, mock_open.return_value)
    mock_find_sources.assert_called_once_with(tmp_path, repo=mock_git_repo.return_value)
    assert result.exit_code == 0
