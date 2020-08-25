from pathlib import Path
from unittest.mock import Mock

import pytest
import toml
from click.testing import CliRunner

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
def mock_install_if_missing(monkeypatch):
    install_mock = Mock()
    monkeypatch.setattr("statue.cli.commands.install_commands_if_missing", install_mock)
    return install_mock


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
