import random

from statue.cli import statue_cli


def test_config_set_history_size_without_specifying_path(
    mock_configuration_path, mock_build_configuration_from_file, cli_runner
):
    size = random.randint(1, 100)
    configuration = mock_build_configuration_from_file.return_value
    configuration.cache.history_size = None

    result = cli_runner.invoke(statue_cli, ["config", "set-history-size", str(size)])

    assert result.exit_code == 0
    assert configuration.cache.history_size == size
    configuration.to_toml.assert_called_once_with(mock_configuration_path.return_value)


def test_config_set_history_size_with_specified_path(
    mock_configuration_path,
    mock_build_configuration_from_file,
    cli_runner,
    tmp_path,
):
    size = random.randint(1, 100)
    config_path = tmp_path / "statue.toml"
    config_path.touch()
    configuration = mock_build_configuration_from_file.return_value
    configuration.cache.history_size = None
    result = cli_runner.invoke(
        statue_cli,
        ["config", "set-history-size", str(size), "--config", str(config_path)],
    )

    assert result.exit_code == 0
    assert configuration.cache.history_size == size
    configuration.to_toml.assert_called_once_with(config_path)
    mock_configuration_path.assert_not_called()
