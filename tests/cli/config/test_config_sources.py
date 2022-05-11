import mock
import pytest

from statue.cli import statue_cli
from statue.cli.config.interactive_adders.interactive_sources_adder import (
    InteractiveSourcesAdder,
)
from statue.commands_filter import CommandsFilter
from tests.constants import COMMAND3, SOURCE1


def test_config_add_source_with_default_path(
    cli_runner, tmp_path, mock_build_configuration_from_file, mock_configuration_path
):
    source = tmp_path / SOURCE1
    source.touch()
    configuration = mock_build_configuration_from_file.return_value
    with mock.patch.object(
        InteractiveSourcesAdder, "update_sources_repository"
    ) as mock_update_sources_repository:
        result = cli_runner.invoke(statue_cli, ["config", "add-source", str(source)])
        mock_update_sources_repository.assert_called_once_with(configuration, [source])

    mock_build_configuration_from_file.assert_called_once_with(
        mock_configuration_path.return_value
    )
    assert result.exit_code == 0


def test_config_add_source_with_path(
    cli_runner, tmp_path, mock_build_configuration_from_file, mock_configuration_path
):
    config_path, source = tmp_path / "statue.toml", tmp_path / SOURCE1
    config_path.touch()
    source.touch()
    configuration = mock_build_configuration_from_file.return_value
    with mock.patch.object(
        InteractiveSourcesAdder, "update_sources_repository"
    ) as mock_update_sources_repository:
        result = cli_runner.invoke(
            statue_cli,
            ["config", "add-source", str(source), "--config", str(config_path)],
        )
        mock_update_sources_repository.assert_called_once_with(configuration, [source])

    mock_build_configuration_from_file.assert_called_once_with(config_path)
    mock_configuration_path.assert_not_called()
    assert result.exit_code == 0


def test_config_edit_source_with_default_configuration_path(
    cli_runner, tmp_path, mock_build_configuration_from_file, mock_configuration_path
):
    source = tmp_path / SOURCE1
    source.touch()
    configuration = mock_build_configuration_from_file.return_value
    configuration.sources_repository[source] = CommandsFilter(allowed_commands=COMMAND3)
    with mock.patch.object(InteractiveSourcesAdder, "get_filter") as mock_get_filter:
        result = cli_runner.invoke(statue_cli, ["config", "edit-source", str(source)])
        mock_get_filter.assert_called_once_with(
            configuration=configuration, source=source
        )
        assert configuration.sources_repository[source] == mock_get_filter.return_value

    mock_build_configuration_from_file.assert_called_once_with(
        mock_configuration_path.return_value
    )
    assert result.exit_code == 0


def test_config_edit_source_with_configuration_path(
    cli_runner, tmp_path, mock_build_configuration_from_file, mock_configuration_path
):
    config_path, source = tmp_path / "statue.toml", tmp_path / SOURCE1
    config_path.touch()
    source.touch()
    configuration = mock_build_configuration_from_file.return_value
    configuration.sources_repository[source] = CommandsFilter(allowed_commands=COMMAND3)
    with mock.patch.object(InteractiveSourcesAdder, "get_filter") as mock_get_filter:
        result = cli_runner.invoke(
            statue_cli,
            ["config", "edit-source", str(source), "--config", str(config_path)],
        )
        mock_get_filter.assert_called_once_with(
            configuration=configuration, source=source
        )
        assert configuration.sources_repository[source] == mock_get_filter.return_value

    mock_build_configuration_from_file.assert_called_once_with(config_path)
    mock_configuration_path.assert_not_called()
    assert result.exit_code == 0


def test_config_edit_non_existing_source(
    cli_runner, tmp_path, mock_build_configuration_from_file, mock_configuration_path
):
    source = tmp_path / SOURCE1
    source.touch()
    with mock.patch.object(InteractiveSourcesAdder, "get_filter") as mock_get_filter:
        result = cli_runner.invoke(
            statue_cli,
            ["config", "edit-source", str(source)],
        )
        mock_get_filter.assert_not_called()

    mock_build_configuration_from_file.assert_called_once_with(
        mock_configuration_path.return_value
    )
    assert result.exit_code == 1
    assert result.output == f"{source} is not specified in configuration\n"


def test_config_remove_source_with_default_configuration_path(
    cli_runner, tmp_path, mock_build_configuration_from_file, mock_configuration_path
):
    source = tmp_path / SOURCE1
    source.touch()
    configuration = mock_build_configuration_from_file.return_value
    configuration.sources_repository[source] = CommandsFilter(allowed_commands=COMMAND3)
    result = cli_runner.invoke(
        statue_cli, ["config", "remove-source", str(source)], input="y\n"
    )

    mock_build_configuration_from_file.assert_called_once_with(
        mock_configuration_path.return_value
    )
    assert source not in configuration.sources_repository.sources_list
    assert result.exit_code == 0


def test_config_remove_source_with_configuration_path(
    cli_runner, tmp_path, mock_build_configuration_from_file, mock_configuration_path
):
    config_path, source = tmp_path / "statue.toml", tmp_path / SOURCE1
    config_path.touch()
    source.touch()
    configuration = mock_build_configuration_from_file.return_value
    configuration.sources_repository[source] = CommandsFilter(allowed_commands=COMMAND3)
    result = cli_runner.invoke(
        statue_cli,
        ["config", "remove-source", str(source), "--config", str(config_path)],
        input="y\n",
    )
    mock_build_configuration_from_file.assert_called_once_with(config_path)

    assert source not in configuration.sources_repository.sources_list
    assert result.exit_code == 0


def test_config_remove_non_existing_source_with_default_configuration_path(
    cli_runner, tmp_path, mock_build_configuration_from_file, mock_configuration_path
):
    source = tmp_path / SOURCE1
    source.touch()
    result = cli_runner.invoke(
        statue_cli, ["config", "remove-source", str(source)], input="y\n"
    )

    mock_build_configuration_from_file.assert_called_once_with(
        mock_configuration_path.return_value
    )
    assert result.exit_code == 1
    assert result.output == f"Could not find {source} in configuration.\n"


@pytest.mark.parametrize(argnames="abort_flag", argvalues=["", "n"])
def test_config_remove_source_abort(
    abort_flag,
    cli_runner,
    tmp_path,
    mock_build_configuration_from_file,
    mock_configuration_path,
):
    source = tmp_path / SOURCE1
    source.touch()
    configuration = mock_build_configuration_from_file.return_value
    configuration.sources_repository[source] = CommandsFilter(
        allowed_commands=[COMMAND3]
    )
    result = cli_runner.invoke(
        statue_cli, ["config", "remove-source", str(source)], input=f"{abort_flag}\n"
    )

    mock_build_configuration_from_file.assert_called_once_with(
        mock_configuration_path.return_value
    )
    assert result.exit_code == 0
    assert result.output == (
        f"Are you sure you would like to remove the source {source} "
        f"from configuration? [y/N]: {abort_flag}\n"
        "Abort!\n"
    )
