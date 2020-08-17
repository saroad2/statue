import pytest
import toml


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
def non_existing_commands_configuration(tmpdir):
    return tmpdir / "commands.toml"


@pytest.fixture
def existing_commands_configuration(
    non_existing_commands_configuration, full_commands_settings_with_boolean_contexts
):
    with open(non_existing_commands_configuration, mode="w") as f:
        toml.dump(full_commands_settings_with_boolean_contexts, f)
    return non_existing_commands_configuration
