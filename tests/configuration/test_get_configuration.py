from statue.configuration import get_configuration
from statue.constants import SOURCES


def test_configuration_file_doesnt_exist(
    non_existing_statue_configuration, existing_commands_configuration
):
    config = get_configuration(
        non_existing_statue_configuration, existing_commands_configuration,
    )
    assert config is None, "Configuration should be none"


def test_commands_file_doesnt_exist(
    existing_statue_configuration,
    non_existing_commands_configuration,
    non_empty_sources_config,
):
    config = get_configuration(
        existing_statue_configuration, non_existing_commands_configuration,
    )
    assert (
        config == non_empty_sources_config
    ), "Configuration should be read from configuration"


def test_both_config_files_exist(
    existing_statue_configuration,
    existing_commands_configuration,
    non_empty_sources_config,
    full_commands_settings_with_boolean_contexts,
):
    config = get_configuration(
        existing_statue_configuration, existing_commands_configuration,
    )
    assert config == dict(
        sources=non_empty_sources_config[SOURCES],
        commands=full_commands_settings_with_boolean_contexts,
    ), "Configuration should be read from both configuration files"
