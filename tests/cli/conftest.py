from pathlib import Path

import pytest
import toml
from click.testing import CliRunner

from statue.command import Command
from statue.configuration import Configuration
from statue.constants import COMMANDS, CONTEXTS, OVERRIDE, SOURCES, STATUE
from tests.constants import (
    BOOLEAN_COMMANDS_CONFIGURATION,
    CONTEXTS_CONFIGURATION,
    SOURCES_CONFIGURATION,
)


@pytest.fixture
def cli_runner():
    return CliRunner()


@pytest.fixture
def cwd_mock(mocker, tmpdir):
    cwd = mocker.patch.object(Path, "cwd")
    cwd.return_value = tmpdir
    return tmpdir


@pytest.fixture
def empty_configuration(cwd_mock):
    configuration = {
        STATUE: {OVERRIDE: True},
    }
    toml.dump(configuration, cwd_mock / "statue.toml")
    yield configuration
    Configuration.reset_configuration()


@pytest.fixture
def full_configuration(cwd_mock):
    configuration = {
        STATUE: {OVERRIDE: True},
        COMMANDS: BOOLEAN_COMMANDS_CONFIGURATION,
        SOURCES: SOURCES_CONFIGURATION,
        CONTEXTS: CONTEXTS_CONFIGURATION,
    }
    toml.dump(configuration, cwd_mock / "statue.toml")
    yield configuration
    Configuration.reset_configuration()


@pytest.fixture
def mock_command_execute(mocker):
    return mocker.patch.object(Command, "_run_subprocess")


@pytest.fixture
def mock_load_configuration(mocker, empty_configuration):
    return mocker.patch.object(Configuration, "load_configuration")


@pytest.fixture
def mock_read_command(mocker, mock_load_configuration):
    return mocker.patch.object(Configuration, "read_command")


@pytest.fixture
def mock_read_commands(mocker, mock_load_configuration):
    return mocker.patch.object(Configuration, "read_commands")
