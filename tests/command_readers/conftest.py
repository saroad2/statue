import pytest

from statue.configuration import Configuration
from statue.constants import ARGS, COMMANDS, CONTEXTS, HELP, SOURCES
from tests.constants import (
    ARG1,
    ARG2,
    BOOLEAN_COMMANDS_CONFIGURATION,
    COMMAND1,
    COMMAND_HELP_STRING1,
    CONTEXTS_CONFIGURATION,
    CONTEXTS_INHERITANCE_CONFIGURATION,
    OVERRIDE_COMMANDS_CONFIGURATION,
    SOURCES_CONFIGURATION,
)


@pytest.fixture
def clear_configuration():
    yield
    Configuration.reset_configuration()


@pytest.fixture
def empty_settings(clear_configuration):
    Configuration.statue_configuration = {}
    yield


@pytest.fixture
def non_empty_sources_config():
    return dict(
        contexts={},
        commands={},
        sources=SOURCES_CONFIGURATION,
    )


@pytest.fixture
def one_command_without_args_setting(clear_configuration):
    configuration = {COMMANDS: {COMMAND1: {HELP: COMMAND_HELP_STRING1}}}
    Configuration.statue_configuration = configuration
    return configuration


@pytest.fixture
def configuration_without_commands(clear_configuration):
    configuration = {
        SOURCES: SOURCES_CONFIGURATION,
    }
    Configuration.statue_configuration = configuration
    return configuration


@pytest.fixture
def one_command_with_args_settings(clear_configuration):
    configuration = {
        COMMANDS: {COMMAND1: {HELP: COMMAND_HELP_STRING1, ARGS: [ARG1, ARG2]}}
    }
    Configuration.statue_configuration = configuration
    return configuration


@pytest.fixture
def full_commands_settings_with_boolean_contexts(clear_configuration):
    configuration = {
        CONTEXTS: CONTEXTS_CONFIGURATION,
        SOURCES: SOURCES_CONFIGURATION,
        COMMANDS: BOOLEAN_COMMANDS_CONFIGURATION,
    }
    Configuration.statue_configuration = configuration
    return configuration


@pytest.fixture
def full_commands_settings(clear_configuration):
    configuration = {
        CONTEXTS: CONTEXTS_CONFIGURATION,
        COMMANDS: OVERRIDE_COMMANDS_CONFIGURATION,
    }
    Configuration.statue_configuration = configuration
    return configuration


@pytest.fixture
def commands_settings_with_context_inheritance(clear_configuration):
    configuration = {
        CONTEXTS: CONTEXTS_INHERITANCE_CONFIGURATION,
        COMMANDS: OVERRIDE_COMMANDS_CONFIGURATION,
    }
    Configuration.statue_configuration = configuration
    return configuration


@pytest.fixture
def full_contexts_settings():
    return CONTEXTS_CONFIGURATION
