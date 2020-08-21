import pytest
import toml

from statue.constants import COMMANDS


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
    non_existing_default_configuration, full_commands_settings_with_boolean_contexts
):
    with open(non_existing_default_configuration, mode="w") as f:
        toml.dump({COMMANDS: full_commands_settings_with_boolean_contexts}, f)
    return non_existing_default_configuration
