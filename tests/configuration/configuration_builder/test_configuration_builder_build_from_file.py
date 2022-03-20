import mock
import pytest

from statue.config.configuration_builder import ConfigurationBuilder
from statue.constants import GENERAL, OVERRIDE
from statue.exceptions import MissingConfiguration


def test_configuration_builder_build_with_existing_path(
    tmp_path,
    mock_update_from_config,
    mock_default_configuration_path,
    mock_cache_path,
    mock_toml_load,
):
    mock_default_configuration_path.touch()
    statue_config_path = tmp_path / "statue"
    statue_config_path.touch()
    default_config, statue_config = {"a": 1}, {"b": 2}
    mock_toml_load.side_effect = {
        mock_default_configuration_path: default_config,
        statue_config_path: statue_config,
    }.get
    cache_path = tmp_path / "cache"
    mock_cache_path.return_value = cache_path

    configuration = ConfigurationBuilder.build_configuration_from_file(
        statue_configuration_path=statue_config_path
    )

    assert mock_toml_load.call_count == 2
    assert mock_toml_load.call_args_list == [
        mock.call(statue_config_path),
        mock.call(mock_default_configuration_path),
    ]
    assert mock_update_from_config.call_count == 2
    assert mock_update_from_config.call_args_list == [
        mock.call(configuration=configuration, statue_config=default_config),
        mock.call(configuration=configuration, statue_config=statue_config),
    ]
    mock_cache_path.assert_called_once_with(tmp_path)
    assert configuration.cache.cache_root_directory == cache_path


def test_configuration_builder_build_with_non_existing_path(
    tmp_path,
    mock_update_from_config,
    mock_default_configuration_path,
    mock_cache_path,
    mock_toml_load,
):
    mock_default_configuration_path.touch()
    statue_config_path = tmp_path / "statue"
    default_config = {"a": 1}
    mock_toml_load.return_value = default_config
    cache_path = tmp_path / "cache"
    mock_cache_path.return_value = cache_path

    assert not statue_config_path.exists()

    configuration = ConfigurationBuilder.build_configuration_from_file(
        statue_configuration_path=statue_config_path
    )

    assert mock_toml_load.call_count == 1
    assert mock_toml_load.call_args_list == [mock.call(mock_default_configuration_path)]
    assert mock_update_from_config.call_count == 2
    assert mock_update_from_config.call_args_list == [
        mock.call(configuration=configuration, statue_config=default_config),
        mock.call(configuration=configuration, statue_config={}),
    ]
    mock_cache_path.assert_called_once_with(tmp_path)
    assert configuration.cache.cache_root_directory == cache_path


def test_configuration_builder_build_with_no_config_path(
    tmp_path,
    mock_update_from_config,
    mock_default_configuration_path,
    mock_configuration_path,
    mock_cache_path,
    mock_toml_load,
):
    mock_default_configuration_path.touch()
    statue_config_path = tmp_path / "statue"
    statue_config_path.touch()
    mock_configuration_path.return_value = statue_config_path
    default_config, statue_config = {"a": 1}, {"b": 2}
    mock_toml_load.side_effect = {
        mock_default_configuration_path: default_config,
        statue_config_path: statue_config,
    }.get
    cache_path = tmp_path / "cache"
    mock_cache_path.return_value = cache_path

    configuration = ConfigurationBuilder.build_configuration_from_file()

    assert mock_toml_load.call_count == 2
    assert mock_toml_load.call_args_list == [
        mock.call(statue_config_path),
        mock.call(mock_default_configuration_path),
    ]
    assert mock_update_from_config.call_count == 2
    assert mock_update_from_config.call_args_list == [
        mock.call(configuration=configuration, statue_config=default_config),
        mock.call(configuration=configuration, statue_config=statue_config),
    ]
    mock_configuration_path.assert_called_once_with()
    mock_cache_path.assert_called_once_with(tmp_path)
    assert configuration.cache.cache_root_directory == cache_path


def test_configuration_builder_build_with_override_default(
    tmp_path,
    mock_update_from_config,
    mock_default_configuration_path,
    mock_cache_path,
    mock_toml_load,
):
    mock_default_configuration_path.touch()
    statue_config_path = tmp_path / "statue"
    statue_config_path.touch()
    statue_config = {"b": 2, GENERAL: {OVERRIDE: True}}
    mock_toml_load.return_value = statue_config
    cache_path = tmp_path / "cache"
    mock_cache_path.return_value = cache_path

    configuration = ConfigurationBuilder.build_configuration_from_file(
        statue_configuration_path=statue_config_path
    )

    assert mock_toml_load.call_count == 1
    assert mock_toml_load.call_args_list == [mock.call(statue_config_path)]
    assert mock_update_from_config.call_count == 1
    assert mock_update_from_config.call_args_list == [
        mock.call(configuration=configuration, statue_config=statue_config),
    ]
    mock_cache_path.assert_called_once_with(tmp_path)
    assert configuration.cache.cache_root_directory == cache_path


def test_configuration_builder_build_with_specified_cache(
    tmp_path,
    mock_update_from_config,
    mock_default_configuration_path,
    mock_cache_path,
    mock_toml_load,
):
    mock_default_configuration_path.touch()
    statue_config_path = tmp_path / "statue"
    statue_config_path.touch()
    default_config, statue_config = {"a": 1}, {"b": 2}
    mock_toml_load.side_effect = {
        mock_default_configuration_path: default_config,
        statue_config_path: statue_config,
    }.get
    cache_path = tmp_path / "cache"

    configuration = ConfigurationBuilder.build_configuration_from_file(
        statue_configuration_path=statue_config_path,
        cache_dir=cache_path,
    )

    assert mock_toml_load.call_count == 2
    assert mock_toml_load.call_args_list == [
        mock.call(statue_config_path),
        mock.call(mock_default_configuration_path),
    ]
    assert mock_update_from_config.call_count == 2
    assert mock_update_from_config.call_args_list == [
        mock.call(configuration=configuration, statue_config=default_config),
        mock.call(configuration=configuration, statue_config=statue_config),
    ]
    mock_cache_path.assert_not_called()
    assert configuration.cache.cache_root_directory == cache_path


def test_configuration_builder_build_with_no_existing_configurations(
    tmp_path,
    mock_update_from_config,
    mock_default_configuration_path,
    mock_cache_path,
    mock_toml_load,
):
    statue_config_path = tmp_path / "statue"

    with pytest.raises(
        MissingConfiguration, match="^Statue was unable to load configuration$"
    ):
        ConfigurationBuilder.build_configuration_from_file(
            statue_configuration_path=statue_config_path
        )

    mock_toml_load.assert_not_called()
    mock_update_from_config.assert_not_called()
    mock_cache_path.assert_not_called()
