import pytest

from statue.configuration import Configuration
from statue.exceptions import EmptyConfiguration

DUMMY_CONFIGURATION = {"a": "b"}


def test_get_statue_configuration_from_default(
    clear_configuration, mock_default_configuration
):
    mock_default_configuration.return_value = DUMMY_CONFIGURATION
    statue_configuration = Configuration.statue_configuration()
    assert statue_configuration == DUMMY_CONFIGURATION


def test_get_statue_configuration_from_set_configuration(
    clear_configuration, mock_default_configuration
):
    Configuration.set_statue_configuration(DUMMY_CONFIGURATION)
    mock_default_configuration.return_value = None
    statue_configuration = Configuration.statue_configuration()
    assert statue_configuration == DUMMY_CONFIGURATION


def test_get_statue_configuration_raise_exception(
    clear_configuration, mock_default_configuration
):
    mock_default_configuration.return_value = None
    with pytest.raises(EmptyConfiguration, match="^Statue configuration is empty!$"):
        Configuration.statue_configuration()
