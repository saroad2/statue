from unittest.mock import Mock

import pytest
from pytest_cases import THIS_MODULE, parametrize_with_cases

from statue.configuration import Configuration
from statue.constants import COMMANDS, CONTEXTS, OVERRIDE, STATUE
from statue.excptions import EmptyConfiguration


def case_default_configuration_doesnt_exist():
    default_configuration = None
    statue_configuration = result = {"a": "b"}
    return default_configuration, statue_configuration, result


def case_configuration_with_override():
    default_configuration = {"a": "b"}
    statue_configuration = result = {"c": "d", STATUE: {OVERRIDE: True}}
    return default_configuration, statue_configuration, result


def case_commands_taken_from_default():
    default_configuration = {COMMANDS: {"a": "b"}}
    statue_configuration = {"c": "d"}
    result = {COMMANDS: {"a": "b"}, "c": "d", CONTEXTS: {}}
    return default_configuration, statue_configuration, result


def case_contexts_taken_from_default():
    default_configuration = {CONTEXTS: {"a": "b"}}
    statue_configuration = {"c": "d"}
    result = {CONTEXTS: {"a": "b"}, "c": "d", COMMANDS: {}}
    return default_configuration, statue_configuration, result


@parametrize_with_cases(
    argnames="default_configuration, statue_configuration, result", cases=THIS_MODULE
)
def test_load_configuration(
    default_configuration,
    statue_configuration,
    result,
    mock_default_configuration,
    mock_toml_load,
    clear_configuration,
):
    statue_path = Mock()
    statue_path.exists.return_value = True
    mock_default_configuration.return_value = default_configuration
    mock_toml_load.return_value = statue_configuration

    Configuration.load_configuration(statue_path)
    assert (
        Configuration.statue_configuration() == result
    ), "Configuration is different than expected."


def test_load_configuration_fail(mock_default_configuration):
    mock_default_configuration.return_value = None
    statue_path = Mock()
    statue_path.exists.return_value = False

    Configuration.load_configuration(statue_path)
    with pytest.raises(EmptyConfiguration, match="^Statue configuration is empty!$"):
        Configuration.statue_configuration()
