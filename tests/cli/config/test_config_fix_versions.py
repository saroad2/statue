from unittest import mock

from statue.cli.cli import statue_cli
from statue.constants import SOURCES, CONTEXTS, COMMANDS, VERSION
from tests.constants import COMMAND1, COMMAND2, SOURCE1, CONTEXT1, SOURCE2, CONTEXT2, CONTEXT3, VERSION1, VERSION2
from tests.util import command_mock


def build_default_toml():
    return {
        SOURCES: {
            SOURCE1: {
                CONTEXTS: [CONTEXT1]
            },
            SOURCE2: {
                CONTEXTS: [CONTEXT2, CONTEXT3]
            }
        }
    }


def test_config_fix_version_with_no_installed_packages(
  cli_runner, mock_cwd, mock_read_commands, mock_toml_load, mock_toml_dump,
):
    command1, command2 = (
        command_mock(name=COMMAND1, installed=False),
        command_mock(name=COMMAND2, installed=False),
    )
    mock_read_commands.return_value = [command1, command2]
    mock_toml_load.return_value = build_default_toml()

    mock_open = mock.mock_open()
    with mock.patch("statue.cli.config.open", mock_open):
        result = cli_runner.invoke(statue_cli, ["config", "fix-versions"])
        mock_toml_load.assert_called_once_with(mock_open.return_value)
        mock_toml_dump.assert_called_once_with(
            {
                COMMANDS: {}, **build_default_toml()
            },
            mock_open.return_value
        )

    assert result.exit_code == 0


def test_config_fix_version_with_one_installed_package(
  cli_runner, mock_cwd, mock_read_commands, mock_toml_load, mock_toml_dump,
):
    version1 = VERSION1
    command1, command2 = (
        command_mock(name=COMMAND1, installed=True, installed_version=version1),
        command_mock(name=COMMAND2, installed=False),
    )
    mock_read_commands.return_value = [command1, command2]
    mock_toml_load.return_value = build_default_toml()

    mock_open = mock.mock_open()
    with mock.patch("statue.cli.config.open", mock_open):
        result = cli_runner.invoke(statue_cli, ["config", "fix-versions"])
        mock_toml_load.assert_called_once_with(mock_open.return_value)
        mock_toml_dump.assert_called_once_with(
            {
                COMMANDS: {
                    COMMAND1: {
                        VERSION: VERSION1
                    }
                },
                **build_default_toml(),
            },
            mock_open.return_value
        )

    assert result.exit_code == 0


def test_config_fix_version_with_two_installed_packages(
  cli_runner, mock_cwd, mock_read_commands, mock_toml_load, mock_toml_dump,
):
    version1, version2 = VERSION1, VERSION2
    command1, command2 = (
        command_mock(name=COMMAND1, installed=True, installed_version=version1),
        command_mock(name=COMMAND2, installed=True, installed_version=version2),
    )
    mock_read_commands.return_value = [command1, command2]
    mock_toml_load.return_value = build_default_toml()

    mock_open = mock.mock_open()
    with mock.patch("statue.cli.config.open", mock_open):
        result = cli_runner.invoke(statue_cli, ["config", "fix-versions"])
        mock_toml_load.assert_called_once_with(mock_open.return_value)
        mock_toml_dump.assert_called_once_with(
            {
                COMMANDS: {
                    COMMAND1: {
                        VERSION: VERSION1
                    },
                    COMMAND2: {
                        VERSION: VERSION2
                    }
                },
                **build_default_toml(),
            },
            mock_open.return_value
        )

    assert result.exit_code == 0


def test_config_fix_version_with_no_commands(
  cli_runner, mock_cwd, mock_read_commands, mock_toml_load, mock_toml_dump,
):
    mock_read_commands.return_value = []
    mock_toml_load.return_value = build_default_toml()

    result = cli_runner.invoke(statue_cli, ["config", "fix-versions"])
    mock_toml_load.assert_not_called()
    mock_toml_dump.assert_not_called()

    assert result.exit_code == 0


def test_config_fix_version_latest(
  cli_runner, mock_cwd, mock_read_commands, mock_toml_load, mock_toml_dump,
):
    version1, version2 = VERSION1, VERSION2
    command1, command2 = (
        command_mock(name=COMMAND1, installed=True, installed_version=version1),
        command_mock(name=COMMAND2, installed=True, installed_version=version2),
    )
    mock_read_commands.return_value = [command1, command2]
    mock_toml_load.return_value = build_default_toml()

    mock_open = mock.mock_open()
    with mock.patch("statue.cli.config.open", mock_open):
        result = cli_runner.invoke(statue_cli, ["config", "fix-versions", "--latest"])
        mock_toml_load.assert_called_once_with(mock_open.return_value)
        mock_toml_dump.assert_called_once_with(
            {
                COMMANDS: {
                    COMMAND1: {
                        VERSION: VERSION1
                    },
                    COMMAND2: {
                        VERSION: VERSION2
                    }
                },
                **build_default_toml(),
            },
            mock_open.return_value
        )
    command1.update.assert_called_once()
    command2.update.assert_called_once()

    assert result.exit_code == 0


def test_config_fix_version_with_direction(
  cli_runner, tmp_path, mock_cwd, mock_read_commands, mock_toml_load, mock_toml_dump,
):
    version1 = VERSION1
    command1, command2 = (
        command_mock(name=COMMAND1, installed=True, installed_version=version1),
        command_mock(name=COMMAND2, installed=False),
    )
    mock_read_commands.return_value = [command1, command2]
    mock_toml_load.return_value = build_default_toml()

    mock_open = mock.mock_open()
    with mock.patch("statue.cli.config.open", mock_open):
        result = cli_runner.invoke(statue_cli, ["config", "fix-versions", "--directory", str(tmp_path)])
        mock_toml_load.assert_called_once_with(mock_open.return_value)
        mock_toml_dump.assert_called_once_with(
            {
                COMMANDS: {
                    COMMAND1: {
                        VERSION: VERSION1
                    }
                },
                **build_default_toml(),
            },
            mock_open.return_value
        )

    assert result.exit_code == 0