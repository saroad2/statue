from pathlib import Path

import pytest
from statue.constants import HELP, ARGS, STANDARD, CLEAR_ARGS, ADD_ARGS

SETTINGS_FILE_PATH = "settings"


COMMAND1, HELP_STRING1 = "command1", "This is a help string for command1"
COMMAND2, HELP_STRING2 = "command2", "This is a help string for command2"
COMMAND3, HELP_STRING3 = "command3", "This is a help string for command3"
COMMAND4, HELP_STRING4 = "command4", "This is a help string for command4"
COMMAND5, HELP_STRING5 = "command5", "This is a help string for command5"
ARG1, ARG2, ARG3, ARG4, ARG5 = "arg1", "arg2", "arg3", "arg4", "arg5"
CONTEXT1, CONTEXT2, CONTEXT3, CONTEXT4 = "context1", "context2", "context3", "context4"
NOT_EXISTING_CONTEXT = "not_existing_context"


@pytest.fixture
def toml(mocker):
    toml_mock = mocker.patch("toml.load")
    yield toml_mock
    toml_mock.assert_called_with(Path(SETTINGS_FILE_PATH))


@pytest.fixture
def empty_settings(toml):
    toml.return_value = {}


@pytest.fixture
def one_command_setting(toml):
    toml.return_value = {COMMAND1: {HELP: HELP_STRING1}}


@pytest.fixture
def one_command_with_args_settings(toml):
    toml.return_value = {COMMAND1: {HELP: HELP_STRING1, ARGS: [ARG1, ARG2]}}


@pytest.fixture
def full_settings_with_boolean_contexts(toml):
    toml.return_value = {
        COMMAND1: {
            HELP: HELP_STRING1,
            ARGS: [ARG1, ARG2],
            CONTEXT1: True,
            CONTEXT2: True,
        },
        COMMAND2: {HELP: HELP_STRING2, ARGS: [ARG3], CONTEXT2: True},
        COMMAND3: {HELP: HELP_STRING3, CONTEXT3: True},
        COMMAND4: {HELP: HELP_STRING4, ARGS: [ARG4, ARG5]},
        COMMAND5: {HELP: HELP_STRING5, STANDARD: False, CONTEXT4: True},
    }


@pytest.fixture
def full_settings_with_override_contexts(toml):
    toml.return_value = {
        COMMAND1: {
            HELP: HELP_STRING1,
            ARGS: [ARG1, ARG2],
            CONTEXT1: {ARGS: [ARG3]},
            CONTEXT2: {ARGS: [ARG4, ARG5]},
            CONTEXT3: {CLEAR_ARGS: True},
            CONTEXT4: {ADD_ARGS: [ARG5]},
        },
    }
