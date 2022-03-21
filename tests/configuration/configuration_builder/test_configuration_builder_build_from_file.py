import pytest

from statue.config.configuration_builder import ConfigurationBuilder
from statue.exceptions import MissingConfiguration


def test_configuration_builder_build_with_existing_path(
    tmp_path,
    mock_update_from_config,
    mock_cache_path,
    mock_toml_load,
    mock_cwd,
):
    statue_config_path = tmp_path / "statue"
    statue_config_path.touch()
    statue_config = ({"a": 1},)
    mock_toml_load.return_value = statue_config
    cache_path = tmp_path / "cache"
    mock_cache_path.return_value = cache_path

    configuration = ConfigurationBuilder.build_configuration_from_file(
        statue_configuration_path=statue_config_path
    )

    mock_toml_load.assert_called_once()
    mock_update_from_config(configuration=configuration, statue_config=statue_config)
    mock_cache_path.assert_called_once_with(mock_cwd)
    assert configuration.cache.cache_root_directory == cache_path


def test_configuration_builder_build_with_no_config_path(
    tmp_path,
    mock_update_from_config,
    mock_configuration_path,
    mock_cache_path,
    mock_toml_load,
    mock_cwd,
):
    mock_configuration_path.return_value.touch()
    statue_config = ({"a": 1},)
    mock_toml_load.return_value = statue_config
    cache_path = tmp_path / "cache"
    mock_cache_path.return_value = cache_path

    configuration = ConfigurationBuilder.build_configuration_from_file()

    mock_toml_load.assert_called_once()
    mock_update_from_config.assert_called_once_with(
        configuration=configuration, statue_config=statue_config
    )
    mock_configuration_path.assert_called_once_with()
    mock_cache_path.assert_called_once_with(mock_cwd)
    assert configuration.cache.cache_root_directory == cache_path


def test_configuration_builder_build_with_specified_cache(
    tmp_path,
    mock_update_from_config,
    mock_cache_path,
    mock_toml_load,
):
    statue_config_path = tmp_path / "statue"
    statue_config_path.touch()
    statue_config = ({"a": 1},)
    mock_toml_load.return_value = statue_config
    cache_path = tmp_path / "cache"

    configuration = ConfigurationBuilder.build_configuration_from_file(
        statue_configuration_path=statue_config_path,
        cache_dir=cache_path,
    )

    mock_toml_load.assert_called_once()
    mock_update_from_config.assert_called_once_with(
        configuration=configuration, statue_config=statue_config
    )
    mock_cache_path.assert_not_called()
    assert configuration.cache.cache_root_directory == cache_path


def test_configuration_builder_build_with_non_existing_path(
    tmp_path,
    mock_update_from_config,
    mock_cache_path,
    mock_toml_load,
):
    statue_config_path = tmp_path / "statue"
    assert not statue_config_path.exists()

    with pytest.raises(
        MissingConfiguration, match="^Statue was unable to load configuration$"
    ):
        ConfigurationBuilder.build_configuration_from_file(
            statue_configuration_path=statue_config_path
        )

    mock_toml_load.assert_not_called()
    mock_update_from_config.assert_not_called()
    mock_cache_path.assert_not_called()
