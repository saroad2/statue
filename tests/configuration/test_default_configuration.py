import pytest

from statue.configuration import Configuration

DUMMY_CONFIGURATION = {"a": "b"}


@pytest.fixture
def mock_default_configuration_path(mocker):
    return mocker.patch("statue.configuration.DEFAULT_CONFIGURATION_FILE")


def test_set_default_configuration(clear_configuration):
    Configuration.set_default_configuration(DUMMY_CONFIGURATION)
    assert (
        Configuration.default_configuration() == DUMMY_CONFIGURATION
    ), "Default configuration was not set"


def test_read_default_configuration_from_file_success(
    clear_configuration, mock_default_configuration_path, mock_toml_load
):
    Configuration.set_default_configuration(None)
    mock_default_configuration_path.exists.return_value = True
    mock_toml_load.return_value = DUMMY_CONFIGURATION
    assert (
        Configuration.default_configuration() == DUMMY_CONFIGURATION
    ), "Default configuration was not set"
    mock_toml_load.assert_called_once_with(mock_default_configuration_path)


def test_read_default_configuration_from_file_failure(
    clear_configuration, mock_default_configuration_path, mock_toml_load
):
    Configuration.set_default_configuration(None)
    mock_default_configuration_path.exists.return_value = False
    assert (
        Configuration.default_configuration() is None
    ), "Default configuration should be None"
    mock_toml_load.assert_not_called()
