import pytest

from statue.configuration import Configuration
from statue.constants import ARGS, COMMANDS, HELP, SOURCES
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
    Configuration.statue_configuration = {}
    yield
    Configuration.reset_configuration()


@pytest.fixture
def non_empty_sources_config():
    return dict(contexts={}, commands={}, sources=SOURCES_CONFIGURATION,)


@pytest.fixture
def one_command_without_args_setting():
    configuration = {COMMANDS: {COMMAND1: {HELP: COMMAND_HELP_STRING1}}}
    Configuration.statue_configuration = configuration
    yield configuration
    Configuration.reset_configuration()


@pytest.fixture
def configuration_without_commands():
    configuration = {
        SOURCES: SOURCES_CONFIGURATION,
    }
    Configuration.statue_configuration = configuration
    yield configuration
    Configuration.reset_configuration()


@pytest.fixture
def one_command_with_args_settings():
    configuration = {
        COMMANDS: {COMMAND1: {HELP: COMMAND_HELP_STRING1, ARGS: [ARG1, ARG2]}}
    }
    Configuration.statue_configuration = configuration
    yield configuration
    Configuration.reset_configuration()


@pytest.fixture
def full_commands_settings_with_boolean_contexts():
    configuration = {
        SOURCES: SOURCES_CONFIGURATION,
        COMMANDS: BOOLEAN_COMMANDS_CONFIGURATION,
    }
    Configuration.statue_configuration = configuration
    yield configuration
    Configuration.reset_configuration()


@pytest.fixture
def full_commands_settings():
    configuration = {COMMANDS: OVERRIDE_COMMANDS_CONFIGURATION}
    Configuration.statue_configuration = configuration
    yield configuration
    Configuration.reset_configuration()


@pytest.fixture
def full_contexts_settings():
    return CONTEXTS_CONFIGURATION
