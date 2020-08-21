import pytest
import toml

from statue.constants import COMMANDS, CONTEXTS


@pytest.fixture
def non_existing_statue_configuration(tmpdir):
    return tmpdir / "statue.toml"


@pytest.fixture
def existing_statue_configuration(
    non_existing_statue_configuration, non_empty_sources_config
):
    with open(non_existing_statue_configuration, mode="w") as f:
        toml.dump(non_empty_sources_config, f)
    return non_existing_statue_configuration


@pytest.fixture
def non_existing_default_configuration(tmpdir):
    return tmpdir / "defaults.toml"


@pytest.fixture
def existing_default_configuration(
    non_existing_default_configuration,
    full_commands_settings_with_boolean_contexts,
    full_contexts_settings,
):
    configuration = {
        COMMANDS: full_commands_settings_with_boolean_contexts,
        CONTEXTS: full_contexts_settings,
    }
    with open(non_existing_default_configuration, mode="w") as f:
        toml.dump(configuration, f)
    return non_existing_default_configuration
