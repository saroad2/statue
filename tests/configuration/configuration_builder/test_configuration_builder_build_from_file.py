import pytest

from statue.config.configuration_builder import ConfigurationBuilder
from statue.exceptions import MissingConfiguration


@pytest.fixture
def mock_configuration_from_dict(mocker):
    return mocker.patch.object(ConfigurationBuilder, "from_dict")


def test_configuration_builder_build_with_existing_path(
    tmp_path,
    mock_configuration_from_dict,
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

    configuration = ConfigurationBuilder.from_file(config_path=statue_config_path)

    assert configuration == mock_configuration_from_dict.return_value
    mock_toml_load.assert_called_once()
    mock_configuration_from_dict.assert_called_once_with(
        statue_config_dict=statue_config, cache_dir=cache_path
    )
    mock_cache_path.assert_called_once_with(mock_cwd)


def test_configuration_builder_build_with_no_config_path(
    tmp_path,
    mock_configuration_from_dict,
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

    configuration = ConfigurationBuilder.from_file()

    assert configuration == mock_configuration_from_dict.return_value
    mock_toml_load.assert_called_once()
    mock_configuration_from_dict.assert_called_once_with(
        cache_dir=cache_path, statue_config_dict=statue_config
    )
    mock_configuration_path.assert_called_once_with()
    mock_cache_path.assert_called_once_with(mock_cwd)


def test_configuration_builder_build_with_specified_cache(
    tmp_path,
    mock_configuration_from_dict,
    mock_cache_path,
    mock_toml_load,
):
    statue_config_path = tmp_path / "statue"
    statue_config_path.touch()
    statue_config = ({"a": 1},)
    mock_toml_load.return_value = statue_config
    cache_path = tmp_path / "cache"

    configuration = ConfigurationBuilder.from_file(
        config_path=statue_config_path,
        cache_dir=cache_path,
    )

    assert configuration == mock_configuration_from_dict.return_value
    mock_toml_load.assert_called_once()
    mock_configuration_from_dict.assert_called_once_with(
        cache_dir=cache_path, statue_config_dict=statue_config
    )
    mock_cache_path.assert_not_called()


def test_configuration_builder_build_with_non_existing_path(
    tmp_path,
    mock_configuration_from_dict,
    mock_cache_path,
    mock_toml_load,
):
    statue_config_path = tmp_path / "statue"
    assert not statue_config_path.exists()

    with pytest.raises(
        MissingConfiguration, match="^Statue was unable to load configuration$"
    ):
        ConfigurationBuilder.from_file(config_path=statue_config_path)

    mock_toml_load.assert_not_called()
    mock_configuration_from_dict.assert_not_called()
    mock_cache_path.assert_not_called()
