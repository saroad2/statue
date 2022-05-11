import mock
import pytest

from statue.cli import statue_cli
from statue.cli.config.interactive_adders.interactive_command_adder import (
    InteractiveCommandAdder,
)
from statue.exceptions import UnknownCommand
from tests.constants import COMMAND1


def test_config_add_command_with_default_path(
    cli_runner, mock_build_configuration_from_file, mock_configuration_path
):
    configuration = mock_build_configuration_from_file.return_value
    with mock.patch.object(InteractiveCommandAdder, "add_command") as mock_add_command:
        result = cli_runner.invoke(statue_cli, ["config", "add-command"])
        mock_add_command.assert_called_once_with(configuration)

    mock_build_configuration_from_file.assert_called_once_with(
        mock_configuration_path.return_value
    )
    assert result.exit_code == 0


def test_config_add_command_with_path(
    cli_runner, mock_build_configuration_from_file, mock_configuration_path, tmp_path
):
    config_path = tmp_path / "statue.toml"
    config_path.touch()
    configuration = mock_build_configuration_from_file.return_value
    with mock.patch.object(InteractiveCommandAdder, "add_command") as mock_add_command:
        result = cli_runner.invoke(
            statue_cli, ["config", "add-command", "--config", str(config_path)]
        )
        mock_add_command.assert_called_once_with(configuration)

    mock_build_configuration_from_file.assert_called_once_with(config_path)
    mock_configuration_path.assert_not_called()
    assert result.exit_code == 0


def test_config_edit_command_with_default_path(
    cli_runner, mock_build_configuration_from_file, mock_configuration_path
):
    configuration = mock_build_configuration_from_file.return_value
    with mock.patch.object(
        InteractiveCommandAdder, "edit_command"
    ) as mock_edit_command:
        result = cli_runner.invoke(statue_cli, ["config", "edit-command", COMMAND1])
        mock_edit_command.assert_called_once_with(
            name=COMMAND1, configuration=configuration
        )

    mock_build_configuration_from_file.assert_called_once_with(
        mock_configuration_path.return_value
    )
    assert result.exit_code == 0


def test_config_edit_command_with_path(
    cli_runner, mock_build_configuration_from_file, mock_configuration_path, tmp_path
):
    config_path = tmp_path / "statue.toml"
    config_path.touch()
    configuration = mock_build_configuration_from_file.return_value
    with mock.patch.object(
        InteractiveCommandAdder, "edit_command"
    ) as mock_edit_command:
        result = cli_runner.invoke(
            statue_cli,
            ["config", "edit-command", COMMAND1, "--config", str(config_path)],
        )
        mock_edit_command.assert_called_once_with(
            name=COMMAND1, configuration=configuration
        )

    mock_build_configuration_from_file.assert_called_once_with(config_path)
    mock_configuration_path.assert_not_called()
    assert result.exit_code == 0


def test_config_remove_command_with_default_path(
    cli_runner, mock_build_configuration_from_file, mock_configuration_path
):
    mock_build_configuration_from_file.return_value = configuration = mock.MagicMock()
    command = configuration.commands_repository.__getitem__.return_value
    result = cli_runner.invoke(
        statue_cli, ["config", "remove-command", COMMAND1], input="y\n"
    )
    configuration.commands_repository.__getitem__.assert_called_once_with(COMMAND1)
    configuration.remove_command.assert_called_once_with(command)

    mock_build_configuration_from_file.assert_called_once_with(
        mock_configuration_path.return_value
    )
    assert result.exit_code == 0


def test_config_remove_command_with_path(
    cli_runner, mock_build_configuration_from_file, mock_configuration_path, tmp_path
):
    config_path = tmp_path / "statue.toml"
    config_path.touch()
    mock_build_configuration_from_file.return_value = configuration = mock.MagicMock()
    command = configuration.commands_repository.__getitem__.return_value
    result = cli_runner.invoke(
        statue_cli,
        ["config", "remove-command", COMMAND1, "--config", str(config_path)],
        input="y\n",
    )
    configuration.commands_repository.__getitem__.assert_called_once_with(COMMAND1)
    configuration.remove_command.assert_called_once_with(command)

    mock_build_configuration_from_file.assert_called_once_with(config_path)
    mock_configuration_path.assert_not_called()
    assert result.exit_code == 0


def test_config_remove_unknown_command_fails(
    cli_runner, mock_build_configuration_from_file, mock_configuration_path, tmp_path
):
    config_path = tmp_path / "statue.toml"
    config_path.touch()
    mock_build_configuration_from_file.return_value = configuration = mock.MagicMock()
    configuration.commands_repository.__getitem__.side_effect = UnknownCommand(COMMAND1)
    result = cli_runner.invoke(
        statue_cli,
        ["config", "remove-command", COMMAND1, "--config", str(config_path)],
    )

    assert result.exit_code == 1
    assert result.output == f'Could not find command named "{COMMAND1}"\n'


@pytest.mark.parametrize(argnames="abort_flag", argvalues=["", "n"])
def test_config_remove_command_abort(
    abort_flag, cli_runner, mock_build_configuration_from_file, mock_configuration_path
):
    mock_build_configuration_from_file.return_value = configuration = mock.MagicMock()
    result = cli_runner.invoke(
        statue_cli, ["config", "remove-command", COMMAND1], input=f"{abort_flag}\n"
    )
    configuration.commands_repository.__getitem__.assert_called_once_with(COMMAND1)
    configuration.remove_command.assert_not_called()

    mock_build_configuration_from_file.assert_called_once_with(
        mock_configuration_path.return_value
    )
    assert result.exit_code == 0
    assert result.output == (
        "Are you sure you would like to remove the command command1 and all of its "
        f"references from configuration? [y/N]: {abort_flag}\n"
        "Abort!\n"
    )
