import git
import mock
import pytest

from statue.cli import statue_cli
from statue.cli.interactive_sources_adder import InteractiveSourcesAdder
from statue.commands_filter import CommandsFilter
from statue.config.configuration import Configuration
from statue.constants import SOURCES
from tests.constants import SOURCE1, SOURCE2, SOURCE3


@pytest.fixture
def mock_git_repo(mocker):
    return mocker.patch("git.Repo")


@pytest.fixture
def mock_update_sources_repository(mocker):
    return mocker.patch.object(InteractiveSourcesAdder, "update_sources_repository")


def test_config_init_simple_case(
    cli_runner,
    mock_configuration_path,
    mock_default_configuration_path,
    mock_update_from_config,
    mock_git_repo,
    mock_cwd,
    mock_update_sources_repository,
    mock_toml_load,
    mock_toml_dump,
    mock_sources_repository_as_dict,
):
    source_path1, source_path2, source_path3 = (
        mock_cwd / f"{SOURCE1}.py",
        mock_cwd / f"{SOURCE2}.py",
        mock_cwd / f"{SOURCE3}.py",
    )
    source_path1.touch()
    source_path2.touch()
    source_path3.touch()
    result = cli_runner.invoke(statue_cli, ["config", "init"])

    assert result.exit_code == 0, f"Exited with exception: {result.exception}"
    mock_configuration_path.assert_called_once_with()
    mock_git_repo.assert_called_once_with(mock_cwd)
    mock_toml_load.assert_called_once_with(mock_default_configuration_path)
    mock_update_from_config.assert_called_once_with(
        mock.ANY, mock_toml_load.return_value
    )
    configuration = mock_update_from_config.call_args_list[0][0][0]
    assert isinstance(configuration, Configuration), f"Configuration of invalid type: {type(configuration).__name__}"
    assert len(configuration.sources_repository) == 3
    assert configuration.sources_repository[source_path1] == CommandsFilter()
    assert configuration.sources_repository[source_path2] == CommandsFilter()
    assert configuration.sources_repository[source_path3] == CommandsFilter()
    mock_update_sources_repository.assert_not_called()
    mock_toml_dump.assert_called_once_with(
        {SOURCES: mock_sources_repository_as_dict.return_value},
        mock.ANY,
    )


def test_config_init_interactive(
    cli_runner,
    mock_configuration_path,
    mock_default_configuration_path,
    mock_update_from_config,
    mock_git_repo,
    mock_cwd,
    mock_update_sources_repository,
    mock_toml_load,
    mock_toml_dump,
    mock_sources_repository_as_dict,
):
    source_path1, source_path2, source_path3 = (
        mock_cwd / f"{SOURCE1}.py",
        mock_cwd / f"{SOURCE2}.py",
        mock_cwd / f"{SOURCE3}.py",
    )
    source_path1.touch()
    source_path2.touch()
    source_path3.touch()
    result = cli_runner.invoke(statue_cli, ["config", "init", "--interactive"])

    assert result.exit_code == 0, f"Exited with exception: {result.exception}"
    mock_configuration_path.assert_called_once_with()
    mock_git_repo.assert_called_once_with(mock_cwd)
    mock_toml_load.assert_called_once_with(mock_default_configuration_path)
    mock_update_from_config.assert_called_once_with(
        mock.ANY, mock_toml_load.return_value
    )
    configuration = mock_update_from_config.call_args_list[0][0][0]
    assert isinstance(configuration, Configuration), f"Configuration of invalid type: {type(configuration).__name__}"
    mock_update_sources_repository.assert_called_once_with(
        configuration=configuration,
        sources=[
            source_path1.relative_to(mock_cwd),
            source_path2.relative_to(mock_cwd),
            source_path3.relative_to(mock_cwd),
        ],
        repo=mock_git_repo.return_value,
    )
    mock_toml_dump.assert_called_once_with(
        {SOURCES: mock_sources_repository_as_dict.return_value},
        mock.ANY,
    )


def test_config_init_without_git(
    cli_runner,
    mock_configuration_path,
    mock_default_configuration_path,
    mock_update_from_config,
    mock_git_repo,
    mock_cwd,
    mock_update_sources_repository,
    mock_toml_load,
    mock_toml_dump,
    mock_sources_repository_as_dict,
):
    source_path1, source_path2, source_path3 = (
        mock_cwd / f"{SOURCE1}.py",
        mock_cwd / f"{SOURCE2}.py",
        mock_cwd / f"{SOURCE3}.py",
    )
    source_path1.touch()
    source_path2.touch()
    source_path3.touch()
    result = cli_runner.invoke(statue_cli, ["config", "init", "--no-git"])

    assert result.exit_code == 0, f"Exited with exception: {result.exception}"
    mock_configuration_path.assert_called_once_with()
    mock_git_repo.assert_not_called()
    mock_toml_load.assert_called_once_with(mock_default_configuration_path)
    mock_update_from_config.assert_called_once_with(
        mock.ANY, mock_toml_load.return_value
    )
    configuration = mock_update_from_config.call_args_list[0][0][0]
    assert isinstance(configuration, Configuration), f"Configuration of invalid type: {type(configuration).__name__}"
    assert len(configuration.sources_repository) == 3
    assert configuration.sources_repository[source_path1] == CommandsFilter()
    assert configuration.sources_repository[source_path2] == CommandsFilter()
    assert configuration.sources_repository[source_path3] == CommandsFilter()
    mock_update_sources_repository.assert_not_called()
    mock_toml_dump.assert_called_once_with(
        {SOURCES: mock_sources_repository_as_dict.return_value},
        mock.ANY,
    )


def test_config_init_interactive_without_git(
    cli_runner,
    mock_configuration_path,
    mock_default_configuration_path,
    mock_update_from_config,
    mock_git_repo,
    mock_cwd,
    mock_update_sources_repository,
    mock_toml_load,
    mock_toml_dump,
    mock_sources_repository_as_dict,
):
    source_path1, source_path2, source_path3 = (
        mock_cwd / f"{SOURCE1}.py",
        mock_cwd / f"{SOURCE2}.py",
        mock_cwd / f"{SOURCE3}.py",
    )
    source_path1.touch()
    source_path2.touch()
    source_path3.touch()
    result = cli_runner.invoke(
        statue_cli, ["config", "init", "--interactive", "--no-git"]
    )

    assert result.exit_code == 0, f"Exited with exception: {result.exception}"
    mock_configuration_path.assert_called_once_with()
    mock_git_repo.assert_not_called()
    mock_toml_load.assert_called_once_with(mock_default_configuration_path)
    mock_update_from_config.assert_called_once_with(
        mock.ANY, mock_toml_load.return_value
    )
    configuration = mock_update_from_config.call_args_list[0][0][0]
    assert isinstance(configuration, Configuration), f"Configuration of invalid type: {type(configuration).__name__}"
    mock_update_sources_repository.assert_called_once_with(
        configuration=configuration,
        sources=[
            source_path1.relative_to(mock_cwd),
            source_path2.relative_to(mock_cwd),
            source_path3.relative_to(mock_cwd),
        ],
        repo=None,
    )
    mock_toml_dump.assert_called_once_with(
        {SOURCES: mock_sources_repository_as_dict.return_value},
        mock.ANY,
    )


def test_config_init_with_git_raises_exception(
    cli_runner,
    mock_configuration_path,
    mock_default_configuration_path,
    mock_update_from_config,
    mock_git_repo,
    mock_cwd,
    mock_update_sources_repository,
    mock_toml_load,
    mock_toml_dump,
    mock_sources_repository_as_dict,
):
    source_path1, source_path2, source_path3 = (
        mock_cwd / f"{SOURCE1}.py",
        mock_cwd / f"{SOURCE2}.py",
        mock_cwd / f"{SOURCE3}.py",
    )
    source_path1.touch()
    source_path2.touch()
    source_path3.touch()
    mock_git_repo.side_effect = git.InvalidGitRepositoryError
    result = cli_runner.invoke(statue_cli, ["config", "init"])

    assert result.exit_code == 0, f"Exited with exception: {result.exception}"
    mock_configuration_path.assert_called_once_with()
    mock_git_repo.assert_called_once_with(mock_cwd)
    mock_toml_load.assert_called_once_with(mock_default_configuration_path)
    mock_update_from_config.assert_called_once_with(
        mock.ANY, mock_toml_load.return_value
    )
    configuration = mock_update_from_config.call_args_list[0][0][0]
    assert isinstance(configuration, Configuration), f"Configuration of invalid type: {type(configuration).__name__}"
    assert len(configuration.sources_repository) == 3
    assert configuration.sources_repository[source_path1] == CommandsFilter()
    assert configuration.sources_repository[source_path2] == CommandsFilter()
    assert configuration.sources_repository[source_path3] == CommandsFilter()
    mock_update_sources_repository.assert_not_called()
    mock_toml_dump.assert_called_once_with(
        {SOURCES: mock_sources_repository_as_dict.return_value},
        mock.ANY,
    )


def test_config_init_interactive_with_git_raises_exception(
    cli_runner,
    mock_configuration_path,
    mock_default_configuration_path,
    mock_update_from_config,
    mock_git_repo,
    mock_cwd,
    mock_update_sources_repository,
    mock_toml_load,
    mock_toml_dump,
    mock_sources_repository_as_dict,
):
    source_path1, source_path2, source_path3 = (
        mock_cwd / f"{SOURCE1}.py",
        mock_cwd / f"{SOURCE2}.py",
        mock_cwd / f"{SOURCE3}.py",
    )
    source_path1.touch()
    source_path2.touch()
    source_path3.touch()
    mock_git_repo.side_effect = git.InvalidGitRepositoryError
    result = cli_runner.invoke(statue_cli, ["config", "init", "--interactive"])

    assert result.exit_code == 0, f"Exited with exception: {result.exception}"
    mock_configuration_path.assert_called_once_with()
    mock_git_repo.assert_called_once_with(mock_cwd)
    mock_toml_load.assert_called_once_with(mock_default_configuration_path)
    mock_update_from_config.assert_called_once_with(
        mock.ANY, mock_toml_load.return_value
    )
    configuration = mock_update_from_config.call_args_list[0][0][0]
    assert isinstance(configuration, Configuration), f"Configuration of invalid type: {type(configuration).__name__}"
    mock_update_sources_repository.assert_called_once_with(
        configuration=configuration,
        sources=[
            source_path1.relative_to(mock_cwd),
            source_path2.relative_to(mock_cwd),
            source_path3.relative_to(mock_cwd),
        ],
        repo=None,
    )
    mock_toml_dump.assert_called_once_with(
        {SOURCES: mock_sources_repository_as_dict.return_value},
        mock.ANY,
    )
