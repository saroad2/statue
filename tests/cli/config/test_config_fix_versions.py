from statue.cli.cli import statue_cli
from tests.constants import COMMAND1, COMMAND2
from tests.util import command_builder_mock, dummy_version, dummy_versions


def test_config_fix_version_with_no_installed_packages(
    cli_runner, mock_build_configuration_from_file, mock_configuration_path
):
    command_builder1, command_builder2 = (
        command_builder_mock(name=COMMAND1, installed=False),
        command_builder_mock(name=COMMAND2, installed=False),
    )
    configuration = mock_build_configuration_from_file.return_value
    configuration.commands_repository.add_command_builders(
        command_builder1, command_builder2
    )

    result = cli_runner.invoke(statue_cli, ["config", "fix-versions"])
    configuration.to_toml.assert_called_once_with(mock_configuration_path.return_value)
    assert result.exit_code == 0
    assert command_builder1.version is None
    assert command_builder2.version is None


def test_config_fix_version_with_one_installed_package(
    cli_runner,
    mock_build_configuration_from_file,
    mock_configuration_path,
):
    version1 = dummy_version()
    command_builder1, command_builder2 = (
        command_builder_mock(name=COMMAND1, installed=True, installed_version=version1),
        command_builder_mock(name=COMMAND2, installed=False),
    )
    configuration = mock_build_configuration_from_file.return_value
    configuration.commands_repository.add_command_builders(
        command_builder1, command_builder2
    )

    result = cli_runner.invoke(statue_cli, ["config", "fix-versions"])

    configuration.to_toml.assert_called_once_with(mock_configuration_path.return_value)
    assert result.exit_code == 0
    assert command_builder1.version == version1
    assert command_builder2.version is None


def test_config_fix_version_with_two_installed_packages(
    cli_runner,
    mock_build_configuration_from_file,
    mock_configuration_path,
):
    version1, version2 = dummy_versions(2)
    command_builder1, command_builder2 = (
        command_builder_mock(name=COMMAND1, installed=True, installed_version=version1),
        command_builder_mock(name=COMMAND2, installed=True, installed_version=version2),
    )
    configuration = mock_build_configuration_from_file.return_value
    configuration.commands_repository.add_command_builders(
        command_builder1, command_builder2
    )

    result = cli_runner.invoke(statue_cli, ["config", "fix-versions"])

    configuration.to_toml.assert_called_once_with(mock_configuration_path.return_value)

    assert result.exit_code == 0
    assert command_builder1.version == version1
    assert command_builder2.version == version2


def test_config_fix_version_with_no_commands(
    cli_runner,
    mock_configuration_path,
    mock_build_configuration_from_file,
):
    result = cli_runner.invoke(statue_cli, ["config", "fix-versions"])

    configuration = mock_build_configuration_from_file.return_value
    configuration.to_toml.assert_not_called()

    assert (
        result.exit_code == 0
    ), f"Existed with failure code and exception: {result.exception}"


def test_config_fix_version_latest(
    cli_runner,
    mock_build_configuration_from_file,
    mock_configuration_path,
):
    version1, version2 = dummy_versions(2)
    command_builder1, command_builder2 = (
        command_builder_mock(name=COMMAND1, installed=True, installed_version=version1),
        command_builder_mock(name=COMMAND2, installed=True, installed_version=version2),
    )
    configuration = mock_build_configuration_from_file.return_value
    configuration.commands_repository.add_command_builders(
        command_builder1, command_builder2
    )

    result = cli_runner.invoke(statue_cli, ["config", "fix-versions", "--latest"])

    configuration.to_toml.assert_called_once_with(mock_configuration_path.return_value)
    command_builder1.update.assert_called_once()
    command_builder2.update.assert_called_once()

    assert result.exit_code == 0
    assert command_builder1.version == version1
    assert command_builder2.version == version2


def test_config_fix_version_with_configuration_path(
    cli_runner,
    mock_build_configuration_from_file,
    tmp_path,
    mock_configuration_path,
):
    config_path = tmp_path / "statue.toml"
    config_path.touch()
    version1 = dummy_version()
    command_builder1, command_builder2 = (
        command_builder_mock(name=COMMAND1, installed=True, installed_version=version1),
        command_builder_mock(name=COMMAND2, installed=False),
    )
    configuration = mock_build_configuration_from_file.return_value
    configuration.commands_repository.add_command_builders(
        command_builder1, command_builder2
    )

    result = cli_runner.invoke(
        statue_cli, ["config", "fix-versions", "--config", str(config_path)]
    )

    configuration.to_toml.assert_called_once_with(config_path)
    assert (
        result.exit_code == 0
    ), f"Exited with error code and exception: {result.exception}"
    assert command_builder1.version == version1
    assert command_builder2.version is None
