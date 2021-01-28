from pathlib import Path
from unittest import mock
from unittest.mock import call

import pytest
from pytest_cases import THIS_MODULE, fixture, parametrize_with_cases

from statue.configuration import Configuration
from statue.constants import (
    ADD_ARGS,
    ARGS,
    CLEAR_ARGS,
    COMMANDS,
    CONTEXTS,
    HELP,
    OVERRIDE,
    SOURCES,
    STATUE,
)
from statue.context import Context
from statue.exceptions import EmptyConfiguration, InvalidStatueConfiguration
from tests.constants import (
    ARG1,
    ARG2,
    ARG3,
    ARG5,
    COMMAND1,
    COMMAND2,
    COMMAND_HELP_STRING1,
    CONTEXT1,
    CONTEXT2,
    CONTEXT_HELP_STRING1,
    CONTEXT_HELP_STRING2,
    SOURCE1,
    SOURCE2,
)
from tests.util import build_contexts_map


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


def case_success_user_override_command_args():
    default_configuration = {COMMANDS: {COMMAND1: {ARGS: [ARG1, ARG2]}}}
    statue_configuration = {COMMANDS: {COMMAND1: {ARGS: [ARG3, ARG5]}}}
    result = {COMMANDS: {COMMAND1: {ARGS: [ARG3, ARG5]}}}
    return default_configuration, statue_configuration, result


def case_success_user_add_command_args():
    default_configuration = {COMMANDS: {COMMAND1: {ARGS: [ARG1, ARG2]}}}
    statue_configuration = {COMMANDS: {COMMAND1: {ADD_ARGS: [ARG3, ARG5]}}}
    result = {COMMANDS: {COMMAND1: {ARGS: [ARG1, ARG2, ARG3, ARG5]}}}
    return default_configuration, statue_configuration, result


def case_success_user_clear_command_args():
    default_configuration = {COMMANDS: {COMMAND1: {ARGS: [ARG1, ARG2]}}}
    statue_configuration = {COMMANDS: {COMMAND1: {CLEAR_ARGS: True}}}
    result = {COMMANDS: {COMMAND1: {}}}
    return default_configuration, statue_configuration, result


def case_success_command_args_are_not_affected():
    default_configuration = {COMMANDS: {COMMAND1: {ARGS: [ARG1, ARG2]}}}
    statue_configuration = {COMMANDS: {COMMAND1: {HELP: COMMAND_HELP_STRING1}}}
    result = {COMMANDS: {COMMAND1: {ARGS: [ARG1, ARG2], HELP: COMMAND_HELP_STRING1}}}
    return default_configuration, statue_configuration, result


def case_success_contexts_taken_from_default():
    contexts_map = build_contexts_map(Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1))
    default_configuration = {CONTEXTS: contexts_map}
    statue_configuration = {"c": "d"}
    result = {CONTEXTS: contexts_map, "c": "d"}
    return default_configuration, statue_configuration, result


def case_success_contexts_taken_from_user():
    default_configuration = {}
    statue_configuration = {
        "c": "d",
        CONTEXTS: {CONTEXT1: {HELP: CONTEXT_HELP_STRING1}},
    }
    result = {
        CONTEXTS: build_contexts_map(Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)),
        "c": "d",
    }
    return default_configuration, statue_configuration, result


def case_success_user_add_new_context():
    context1 = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    default_configuration = {CONTEXTS: build_contexts_map(context1)}
    statue_configuration = {
        "c": "d",
        CONTEXTS: {CONTEXT2: {HELP: CONTEXT_HELP_STRING2}},
    }
    result = {
        CONTEXTS: build_contexts_map(
            context1,
            Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2),
        ),
        "c": "d",
    }
    return default_configuration, statue_configuration, result


def case_success_read_sources():
    default_configuration = {}
    statue_configuration = {
        SOURCES: {SOURCE1: {CONTEXTS: [CONTEXT1]}, SOURCE2: {CONTEXTS: [CONTEXT1]}}
    }
    result = {
        SOURCES: {
            Path(SOURCE1): {CONTEXTS: [CONTEXT1]},
            Path(SOURCE2): {CONTEXTS: [CONTEXT1]},
        }
    }
    return default_configuration, statue_configuration, result


@parametrize_with_cases(
    argnames=["default_configuration", "statue_configuration", "result"],
    cases=THIS_MODULE,
    prefix="case_success_",
)
def test_load_configuration_from_file_as_path_successful(
    default_configuration,
    statue_configuration,
    result,
    mock_default_configuration,
    mock_toml_load,
    tmpdir,
    clear_configuration,
):
    statue_path = Path(tmpdir) / "configuration.toml"
    statue_path.touch()
    mock_default_configuration.return_value = default_configuration
    mock_toml_load.return_value = statue_configuration

    Configuration.load_configuration(statue_path)
    assert (
        Configuration.statue_configuration() == result
    ), "Configuration is different than expected."
    mock_toml_load.assert_called_with(statue_path)


@parametrize_with_cases(
    argnames="default_configuration, statue_configuration, result",
    cases=THIS_MODULE,
    prefix="case_success_",
)
def test_load_configuration_from_file_as_string_successful(
    default_configuration,
    statue_configuration,
    result,
    mock_default_configuration,
    mock_toml_load,
    tmpdir,
    clear_configuration,
):
    statue_path = Path(tmpdir) / "configuration.toml"
    statue_path.touch()
    mock_default_configuration.return_value = default_configuration
    mock_toml_load.return_value = statue_configuration

    Configuration.load_configuration(str(statue_path))
    assert (
        Configuration.statue_configuration() == result
    ), "Configuration is different than expected."
    mock_toml_load.assert_called_with(statue_path)


@parametrize_with_cases(
    argnames="default_configuration, statue_configuration, result",
    cases=THIS_MODULE,
    prefix="case_success_",
)
def test_load_configuration_from_default_path_successful(
    default_configuration,
    statue_configuration,
    result,
    mock_default_configuration,
    mock_toml_load,
    mock_cwd,
    clear_configuration,
):
    statue_path = mock_cwd / "statue.toml"
    statue_path.touch()
    mock_default_configuration.return_value = default_configuration
    mock_toml_load.return_value = statue_configuration

    Configuration.load_configuration()
    assert (
        Configuration.statue_configuration() == result
    ), "Configuration is different than expected."
    mock_toml_load.assert_called_with(statue_path)


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
    statue_path = mock.Mock()
    statue_path.exists.return_value = True
    mock_default_configuration.return_value = default_configuration
    mock_toml_load.return_value = statue_configuration

    with pytest.raises(exception_class, match=exception_message):
        Configuration.load_configuration(statue_path)


# Additional cases


def test_load_configuration_fail_because_of_empty_configuration(
    mock_default_configuration,
):
    mock_default_configuration.return_value = None
    statue_path = mock.Mock()
    statue_path.exists.return_value = False

    Configuration.load_configuration(statue_path)
    with pytest.raises(EmptyConfiguration, match="^Statue configuration is empty!$"):
        Configuration.statue_configuration()
