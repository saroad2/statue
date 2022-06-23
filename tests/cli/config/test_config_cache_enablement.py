from statue.cli import statue_cli


def test_config_enable_cache(
    cli_runner, mock_build_configuration_from_file, mock_configuration_path
):
    configuration = mock_build_configuration_from_file.return_value
    configuration.cache.enabled = False

    result = cli_runner.invoke(statue_cli, ["config", "enable-cache"])

    assert result.exit_code == 0
    assert configuration.cache.enabled

    mock_configuration_path.assert_called_once_with()
    configuration.to_toml.assert_called_once_with(mock_configuration_path.return_value)


def test_config_enable_cache_with_config_path(
    cli_runner, mock_build_configuration_from_file, mock_configuration_path, tmp_path
):
    config_path = tmp_path / "statue.toml"
    config_path.touch()
    configuration = mock_build_configuration_from_file.return_value
    configuration.cache.enabled = False

    result = cli_runner.invoke(
        statue_cli, ["config", "enable-cache", "--config", str(config_path)]
    )

    assert result.exit_code == 0
    assert configuration.cache.enabled

    mock_configuration_path.assert_not_called()
    configuration.to_toml.assert_called_once_with(config_path)


def test_config_disable_cache(
    cli_runner, mock_build_configuration_from_file, mock_configuration_path
):
    configuration = mock_build_configuration_from_file.return_value
    configuration.cache.enabled = True

    result = cli_runner.invoke(statue_cli, ["config", "disable-cache"])

    assert result.exit_code == 0
    assert not configuration.cache.enabled

    mock_configuration_path.assert_called_once_with()
    configuration.to_toml.assert_called_once_with(mock_configuration_path.return_value)


def test_config_disable_cache_with_config_path(
    cli_runner, mock_build_configuration_from_file, mock_configuration_path, tmp_path
):
    config_path = tmp_path / "statue.toml"
    config_path.touch()
    configuration = mock_build_configuration_from_file.return_value
    configuration.cache.enabled = True

    result = cli_runner.invoke(
        statue_cli, ["config", "disable-cache", "--config", str(config_path)]
    )

    assert result.exit_code == 0
    assert not configuration.cache.enabled

    mock_configuration_path.assert_not_called()
    configuration.to_toml.assert_called_once_with(config_path)
