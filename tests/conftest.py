from pathlib import Path

import pytest

from statue.configuration import Configuration


@pytest.fixture
def mock_toml_load(mocker):
    return mocker.patch("toml.load")


@pytest.fixture
def mock_toml_dump(mocker):
    return mocker.patch("toml.dump")


@pytest.fixture
def clear_configuration():
    yield
    Configuration.reset_configuration()


@pytest.fixture
def mock_read_command(mocker, clear_configuration):
    return mocker.patch.object(Configuration, "read_command")


@pytest.fixture
def mock_read_commands(mocker, clear_configuration):
    return mocker.patch.object(Configuration, "read_commands")


@pytest.fixture
def mock_commands_names_list(mocker, clear_configuration):
    return mocker.patch.object(Configuration, "commands_names_list")


@pytest.fixture
def mock_default_configuration(mocker, clear_configuration):
    return mocker.patch.object(Configuration, "default_configuration")


@pytest.fixture
def mock_contexts_configuration(mocker, clear_configuration):
    return mocker.patch.object(Configuration, "contexts_configuration")


@pytest.fixture
def mock_sources_configuration(mocker, clear_configuration):
    return mocker.patch.object(Configuration, "sources_configuration")


@pytest.fixture
def mock_load_configuration(mocker, clear_configuration):
    return mocker.patch.object(Configuration, "load_configuration")


@pytest.fixture
def mock_cwd(mocker):
    return mocker.patch.object(Path, "cwd").return_value
