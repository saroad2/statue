import pytest

from statue.constants import ARGS, HELP
from tests.constants import (
    ARG1,
    ARG2,
    BOOLEAN_COMMANDS_CONFIGURATION,
    COMMAND1,
    COMMAND_HELP_STRING1,
    CONTEXTS_CONFIGURATION,
    OVERRIDE_COMMANDS_CONFIGURATION,
    SOURCES_CONFIGURATION,
)


@pytest.fixture
def empty_settings():
    return {}


@pytest.fixture
def non_empty_sources_config():
    return dict(contexts={}, commands={}, sources=SOURCES_CONFIGURATION,)


@pytest.fixture
def one_command_setting():
    return {COMMAND1: {HELP: COMMAND_HELP_STRING1}}


@pytest.fixture
def one_command_with_args_settings():
    return {COMMAND1: {HELP: COMMAND_HELP_STRING1, ARGS: [ARG1, ARG2]}}


@pytest.fixture
def full_commands_settings_with_boolean_contexts():
    return BOOLEAN_COMMANDS_CONFIGURATION


@pytest.fixture
def full_commands_settings():
    return OVERRIDE_COMMANDS_CONFIGURATION


@pytest.fixture
def full_contexts_settings():
    return CONTEXTS_CONFIGURATION
