import os
from pathlib import Path

import pytest

from statue.command import Command
from statue.configuration import Configuration

ENVIRON = dict(s=2, d=5, g=8)


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
def mock_contexts_map(mocker, clear_configuration):
    return mocker.patch.object(Configuration, "contexts_map")


@pytest.fixture
def mock_sources_configuration(mocker, clear_configuration):
    return mocker.patch.object(Configuration, "sources_configuration")


@pytest.fixture
def mock_load_configuration(mocker, clear_configuration):
    return mocker.patch.object(Configuration, "load_configuration")


@pytest.fixture
def mock_cwd(mocker):
    return mocker.patch.object(Path, "cwd").return_value


@pytest.fixture
def mock_subprocess(mocker):
    return mocker.patch("subprocess.run")


@pytest.fixture
def mock_available_packages(mocker):
    return mocker.patch.object(Command, "available_packages")


@pytest.fixture
def environ(monkeypatch):
    monkeypatch.setattr(os, "environ", ENVIRON)
    return ENVIRON


@pytest.fixture
def print_mock(mocker):
    return mocker.patch("builtins.print")