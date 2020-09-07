from unittest.mock import Mock

import pytest
from pytest_cases import THIS_MODULE, parametrize_with_cases

from statue.configuration import Configuration
from statue.constants import COMMANDS, CONTEXTS, OVERRIDE, STATUE
from statue.excptions import EmptyConfiguration
from tests.constants import COMMAND1, COMMAND2, CONTEXT1, CONTEXT2


def case_default_configuration_doesnt_exist():
    default_configuration = None
    statue_configuration = result = {"a": "b"}
    return default_configuration, statue_configuration, result


def case_configuration_with_override():
    default_configuration = {"a": "b"}
    statue_configuration = result = {"c": "d", STATUE: {OVERRIDE: True}}
    return default_configuration, statue_configuration, result


def case_commands_taken_from_default():
    default_configuration = {COMMANDS: {COMMAND1: {CONTEXT1: "b"}}}
    statue_configuration = {"c": "d"}
    result = {COMMANDS: {COMMAND1: {CONTEXT1: "b"}}, "c": "d", CONTEXTS: {}}
    return default_configuration, statue_configuration, result


def case_commands_taken_from_user():
    default_configuration = {}
    statue_configuration = {COMMANDS: {COMMAND1: {CONTEXT1: "b"}}}
    result = {COMMANDS: {COMMAND1: {CONTEXT1: "b"}}, CONTEXTS: {}}
    return default_configuration, statue_configuration, result


def case_contexts_taken_from_default():
    default_configuration = {CONTEXTS: {"a": "b"}}
    statue_configuration = {"c": "d"}
    result = {CONTEXTS: {"a": "b"}, "c": "d"}
    return default_configuration, statue_configuration, result


def case_marge_commands_from_user_and_default():
    default_configuration = {COMMANDS: {COMMAND1: {CONTEXT1: "b"}}}
    statue_configuration = {"c": "d", COMMANDS: {COMMAND2: {"e": "f"}}}
    result = {
        COMMANDS: {COMMAND1: {CONTEXT1: "b"}, COMMAND2: {"e": "f"}},
        "c": "d",
        CONTEXTS: {},
    }
    return default_configuration, statue_configuration, result


def case_user_override_default_command_in_context():
    default_configuration = {COMMANDS: {COMMAND1: {CONTEXT1: "c"}}}
    statue_configuration = {"c": "d", COMMANDS: {COMMAND1: {CONTEXT1: "f"}}}
    result = {COMMANDS: {COMMAND1: {CONTEXT1: "f"}}, "c": "d", CONTEXTS: {}}
    return default_configuration, statue_configuration, result


def case_user_add_context_to_command():
    default_configuration = {COMMANDS: {COMMAND1: {CONTEXT1: "c"}}}
    statue_configuration = {"c": "d", COMMANDS: {COMMAND1: {CONTEXT2: "f"}}}
    result = {
        COMMANDS: {COMMAND1: {CONTEXT1: "c", CONTEXT2: "f"}},
        "c": "d",
        CONTEXTS: {},
    }
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
