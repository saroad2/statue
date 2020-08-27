import pytest

from statue.configuration import Configuration
from statue.constants import COMMANDS, CONTEXTS, OVERRIDE, SOURCES, STATUE
from statue.excptions import EmptyConfiguration
from tests.configuration.conftest import DEFAULT_CONFIG, STATUE_CONFIGURATION
from tests.constants import (
    BOOLEAN_COMMANDS_CONFIGURATION,
    COMMAND1,
    COMMAND2,
    COMMAND3,
    COMMAND4,
    COMMAND5,
    CONTEXTS_CONFIGURATION,
    CONTEXTS_CONFIGURATION2,
    OVERRIDE_COMMANDS_CONFIGURATION,
    SOURCES_CONFIGURATION,
    SOURCES_CONFIGURATION2,
)


def test_configuration_doesnt_exists(non_existing_default_config):
    assert (
        Configuration.default_configuration is None
    ), "Default configuration should be None"

    with pytest.raises(EmptyConfiguration, match="^Statue configuration is empty!$"):
        Configuration.statue_configuration  # pylint: disable=pointless-statement
    with pytest.raises(EmptyConfiguration, match="^Statue configuration is empty!$"):
        Configuration.commands_configuration  # pylint: disable=pointless-statement
    with pytest.raises(EmptyConfiguration, match="^Statue configuration is empty!$"):
        Configuration.commands_names_list  # pylint: disable=pointless-statement
    with pytest.raises(EmptyConfiguration, match="^Statue configuration is empty!$"):
        Configuration.contexts_configuration  # pylint: disable=pointless-statement
    with pytest.raises(EmptyConfiguration, match="^Statue configuration is empty!$"):
        Configuration.sources_configuration  # pylint: disable=pointless-statement


def test_default_configuration_exists_and_empty(existing_empty_default_config):
    assert (
        Configuration.default_configuration == {}
    ), "Default configuration should be empty."
    assert (
        Configuration.statue_configuration == {}
    ), "Statue configuration should be empty."
    assert (
        Configuration.commands_configuration is None
    ), "Commands configuration should be None."
    assert Configuration.commands_names_list == [], "Commands list should be empty."
    assert (
        Configuration.contexts_configuration is None
    ), "Contexts configuration should be None."
    assert (
        Configuration.sources_configuration is None
    ), "Sources configuration should be None."


def test_default_configuration_exists_and_non_empty(existing_non_empty_default_config):
    assert (
        Configuration.default_configuration == DEFAULT_CONFIG
    ), "Default configuration not loaded."
    assert (
        Configuration.statue_configuration == DEFAULT_CONFIG
    ), "Statue configuration is different than expected."
    assert (
        Configuration.commands_configuration == BOOLEAN_COMMANDS_CONFIGURATION
    ), "Commands configuration is different than expected."
    assert Configuration.commands_names_list == [
        COMMAND1,
        COMMAND2,
        COMMAND3,
        COMMAND4,
        COMMAND5,
    ], "Commands list is different than expected."
    assert (
        Configuration.contexts_configuration == CONTEXTS_CONFIGURATION
    ), "Contexts configuration is different than expected."
    assert (
        Configuration.sources_configuration == SOURCES_CONFIGURATION
    ), "Sources configuration is different than expected."


def test_load_non_existing_statue_configuration(
    direct_set_default_config, non_existing_file, existing_non_empty_statue_config
):
    Configuration.load_configuration(non_existing_file)
    assert (
        Configuration.default_configuration == DEFAULT_CONFIG
    ), "Default configuration not loaded."
    assert (
        Configuration.statue_configuration == DEFAULT_CONFIG
    ), "Statue configuration is different than expected."
    assert (
        Configuration.commands_configuration == BOOLEAN_COMMANDS_CONFIGURATION
    ), "Commands configuration is different than expected."
    assert Configuration.commands_names_list == [
        COMMAND1,
        COMMAND2,
        COMMAND3,
        COMMAND4,
        COMMAND5,
    ], "Commands list is different than expected."
    assert (
        Configuration.contexts_configuration == CONTEXTS_CONFIGURATION
    ), "Contexts configuration is different than expected."
    assert (
        Configuration.sources_configuration == SOURCES_CONFIGURATION
    ), "Sources configuration is different than expected."


def test_statue_configuration_different_than_default(
    direct_set_default_config, existing_file, existing_non_empty_statue_config
):
    Configuration.load_configuration(existing_file)
    assert (
        Configuration.default_configuration == DEFAULT_CONFIG
    ), "Default configuration not loaded."
    assert Configuration.statue_configuration == {
        COMMANDS: BOOLEAN_COMMANDS_CONFIGURATION,
        SOURCES: SOURCES_CONFIGURATION2,
        CONTEXTS: CONTEXTS_CONFIGURATION,
    }, "Statue configuration is different than expected."
    assert (
        Configuration.commands_configuration == BOOLEAN_COMMANDS_CONFIGURATION
    ), "Commands configuration is different than expected."
    assert Configuration.commands_names_list == [
        COMMAND1,
        COMMAND2,
        COMMAND3,
        COMMAND4,
        COMMAND5,
    ], "Commands list is different than expected."
    assert (
        Configuration.contexts_configuration == CONTEXTS_CONFIGURATION
    ), "Contexts configuration is different than expected."
    assert (
        Configuration.sources_configuration == SOURCES_CONFIGURATION2
    ), "Sources configuration is different than expected."


def test_statue_configuration_different_than_default_with_general_override(
    direct_set_default_config,
    existing_file,
    existing_non_empty_statue_config_with_general_override,
):
    Configuration.load_configuration(existing_file)
    assert (
        Configuration.default_configuration == DEFAULT_CONFIG
    ), "Default configuration not loaded."
    assert Configuration.statue_configuration == {
        STATUE: {OVERRIDE: True},
        **STATUE_CONFIGURATION,
    }, "Statue configuration is different than expected."
    assert (
        Configuration.commands_configuration == OVERRIDE_COMMANDS_CONFIGURATION
    ), "Commands configuration is different than expected."
    assert Configuration.commands_names_list == [
        COMMAND1,
        COMMAND2,
    ], "Commands list is different than expected."
    assert (
        Configuration.contexts_configuration == CONTEXTS_CONFIGURATION2
    ), "Contexts configuration is different than expected."
    assert (
        Configuration.sources_configuration == SOURCES_CONFIGURATION2
    ), "Sources configuration is different than expected."


def test_statue_configuration_exists_and_default_does_not(
    non_existing_default_config,
    existing_file,
    existing_non_empty_statue_config,
):
    Configuration.load_configuration(existing_file)
    assert (
        Configuration.default_configuration is None
    ), "Default configuration should be None."
    assert (
        Configuration.statue_configuration == STATUE_CONFIGURATION
    ), "Statue configuration is different than expected."
    assert (
        Configuration.commands_configuration == OVERRIDE_COMMANDS_CONFIGURATION
    ), "Commands configuration is different than expected."
    assert Configuration.commands_names_list == [
        COMMAND1,
        COMMAND2,
    ], "Commands list is different than expected."
    assert (
        Configuration.contexts_configuration == CONTEXTS_CONFIGURATION2
    ), "Contexts configuration is different than expected."
    assert (
        Configuration.sources_configuration == SOURCES_CONFIGURATION2
    ), "Sources configuration is different than expected."
