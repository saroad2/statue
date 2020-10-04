from unittest.mock import Mock

import pytest
from pytest_cases import THIS_MODULE, parametrize_with_cases

from statue.configuration import Configuration
from statue.constants import COMMANDS, CONTEXTS, HELP, OVERRIDE, STATUE
from statue.exceptions import EmptyConfiguration, InvalidStatueConfiguration
from tests.constants import (
    COMMAND1,
    COMMAND2,
    CONTEXT1,
    CONTEXT2,
    CONTEXT_HELP_STRING1,
    CONTEXT_HELP_STRING2,
)

# Success cases


def case_success_default_configuration_doesnt_exist():
    default_configuration = None
    statue_configuration = result = {"a": "b"}
    return default_configuration, statue_configuration, result


def case_success_configuration_with_override():
    default_configuration = {"a": "b"}
    statue_configuration = result = {"c": "d", STATUE: {OVERRIDE: True}}
    return default_configuration, statue_configuration, result


def case_success_commands_taken_from_default():
    default_configuration = {COMMANDS: {COMMAND1: {CONTEXT1: "b"}}}
    statue_configuration = {"c": "d"}
    result = {COMMANDS: {COMMAND1: {CONTEXT1: "b"}}, "c": "d"}
    return default_configuration, statue_configuration, result


def case_success_commands_taken_from_user():
    default_configuration = {}
    statue_configuration = {COMMANDS: {COMMAND1: {CONTEXT1: "b"}}}
    result = {COMMANDS: {COMMAND1: {CONTEXT1: "b"}}}
    return default_configuration, statue_configuration, result


def case_success_merge_commands_from_user_and_default():
    default_configuration = {COMMANDS: {COMMAND1: {CONTEXT1: "b"}}}
    statue_configuration = {"c": "d", COMMANDS: {COMMAND2: {"e": "f"}}}
    result = {
        COMMANDS: {COMMAND1: {CONTEXT1: "b"}, COMMAND2: {"e": "f"}},
        "c": "d",
    }
    return default_configuration, statue_configuration, result


def case_success_user_override_default_command_in_context():
    default_configuration = {COMMANDS: {COMMAND1: {CONTEXT1: "c"}}}
    statue_configuration = {"c": "d", COMMANDS: {COMMAND1: {CONTEXT1: "f"}}}
    result = {COMMANDS: {COMMAND1: {CONTEXT1: "f"}}, "c": "d"}
    return default_configuration, statue_configuration, result


def case_success_user_add_context_to_command():
    default_configuration = {COMMANDS: {COMMAND1: {CONTEXT1: "c"}}}
    statue_configuration = {"c": "d", COMMANDS: {COMMAND1: {CONTEXT2: "f"}}}
    result = {
        COMMANDS: {COMMAND1: {CONTEXT1: "c", CONTEXT2: "f"}},
        "c": "d",
    }
    return default_configuration, statue_configuration, result


def case_success_contexts_taken_from_default():
    default_configuration = {CONTEXTS: {"a": "b"}}
    statue_configuration = {"c": "d"}
    result = {CONTEXTS: {"a": "b"}, "c": "d"}
    return default_configuration, statue_configuration, result


def case_success_contexts_taken_from_user():
    default_configuration = {}
    statue_configuration = {"c": "d", CONTEXTS: {"a": "b"}}
    result = {CONTEXTS: {"a": "b"}, "c": "d"}
    return default_configuration, statue_configuration, result


def case_success_user_add_new_context():
    default_configuration = {CONTEXTS: {CONTEXT1: {HELP: CONTEXT_HELP_STRING1}}}
    statue_configuration = {
        "c": "d",
        CONTEXTS: {CONTEXT2: {HELP: CONTEXT_HELP_STRING2}},
    }
    result = {
        CONTEXTS: {
            CONTEXT1: {HELP: CONTEXT_HELP_STRING1},
            CONTEXT2: {HELP: CONTEXT_HELP_STRING2},
        },
        "c": "d",
    }
    return default_configuration, statue_configuration, result


@parametrize_with_cases(
    argnames="default_configuration, statue_configuration, result",
    cases=THIS_MODULE,
    prefix="case_success_",
)
def test_load_configuration_successful(
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


# Failure cases


def case_failure_user_add_new_context():
    default_configuration = {CONTEXTS: {CONTEXT1: {HELP: CONTEXT_HELP_STRING1}}}
    statue_configuration = {CONTEXTS: {CONTEXT1: {HELP: CONTEXT_HELP_STRING2}}}
    exception_class = InvalidStatueConfiguration
    exception_message = f'^"{CONTEXT1}" is a predefined context and cannot be override$'
    return (
        default_configuration,
        statue_configuration,
        exception_class,
        exception_message,
    )


@parametrize_with_cases(
    argnames=(
        "default_configuration, statue_configuration, "
        "exception_class, exception_message"
    ),
    cases=THIS_MODULE,
    prefix="case_failure_",
)
def test_load_configuration_failure(
    default_configuration,
    statue_configuration,
    exception_class,
    exception_message,
    mock_default_configuration,
    mock_toml_load,
    clear_configuration,
):
    statue_path = Mock()
    statue_path.exists.return_value = True
    mock_default_configuration.return_value = default_configuration
    mock_toml_load.return_value = statue_configuration

    with pytest.raises(exception_class, match=exception_message):
        Configuration.load_configuration(statue_path)


# Additional cases


def test_load_configuration_fail(mock_default_configuration):
    mock_default_configuration.return_value = None
    statue_path = Mock()
    statue_path.exists.return_value = False

    Configuration.load_configuration(statue_path)
    with pytest.raises(EmptyConfiguration, match="^Statue configuration is empty!$"):
        Configuration.statue_configuration()
