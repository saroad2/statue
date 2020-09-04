from pathlib import Path

import pytest
import toml

from statue.configuration import Configuration
from statue.constants import OVERRIDE, STATUE


@pytest.fixture
def cwd_mock(mocker, tmpdir):
    cwd = mocker.patch.object(Path, "cwd")
    cwd.return_value = tmpdir
    return tmpdir


@pytest.fixture
def clear_configuration():
    yield
    Configuration.reset_configuration()


@pytest.fixture
def empty_configuration(cwd_mock, clear_configuration):
    configuration = {
        STATUE: {OVERRIDE: True},
    }
    toml.dump(configuration, cwd_mock / "statue.toml")
    return configuration


@pytest.fixture
def mock_read_command(mocker, empty_configuration):
    return mocker.patch.object(Configuration, "read_command")


@pytest.fixture
def mock_read_commands(mocker, empty_configuration):
    return mocker.patch.object(Configuration, "read_commands")


@pytest.fixture
def mock_commands_names_list(mocker, empty_configuration):
    return mocker.patch.object(Configuration, "commands_names_list")


@pytest.fixture
def mock_contexts_configuration(mocker, empty_configuration):
    return mocker.patch.object(Configuration, "contexts_configuration")


@pytest.fixture
def mock_sources_configuration(mocker, empty_configuration):
    return mocker.patch.object(Configuration, "sources_configuration")
