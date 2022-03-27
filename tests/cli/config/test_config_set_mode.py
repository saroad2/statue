import pytest

from statue.cli import statue_cli
from statue.runner import RunnerMode


@pytest.mark.parametrize(argnames="mode", argvalues=[RunnerMode.SYNC, RunnerMode.ASYNC])
def test_config_set_mode_without_specifying_path(
    mode, mock_configuration_path, mock_build_configuration_from_file, cli_runner
):
    configuration = mock_build_configuration_from_file.return_value
    configuration.default_mode = None
    result = cli_runner.invoke(statue_cli, ["config", "set-mode", mode.name])

    assert result.exit_code == 0
    assert configuration.default_mode == mode
    configuration.to_toml.assert_called_once_with(mock_configuration_path.return_value)


@pytest.mark.parametrize(argnames="mode", argvalues=[RunnerMode.SYNC, RunnerMode.ASYNC])
def test_config_set_mode_with_specified_path(
    mode,
    mock_configuration_path,
    mock_build_configuration_from_file,
    cli_runner,
    tmp_path,
):
    config_path = tmp_path / "statue.toml"
    config_path.touch()
    configuration = mock_build_configuration_from_file.return_value
    configuration.default_mode = None
    result = cli_runner.invoke(
        statue_cli, ["config", "set-mode", mode.name, "--config", str(config_path)]
    )

    assert result.exit_code == 0
    assert configuration.default_mode == mode
    configuration.to_toml.assert_called_once_with(config_path)
    mock_configuration_path.assert_not_called()
