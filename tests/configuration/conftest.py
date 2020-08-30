from copy import deepcopy
from unittest.mock import Mock

import pytest

from statue.configuration import Configuration
from statue.constants import COMMANDS, CONTEXTS, OVERRIDE, SOURCES, STATUE
from tests.constants import (
    BOOLEAN_COMMANDS_CONFIGURATION,
    CONTEXTS_CONFIGURATION,
    CONTEXTS_INHERITANCE_CONFIGURATION,
    OVERRIDE_COMMANDS_CONFIGURATION,
    SOURCES_CONFIGURATION,
    SOURCES_CONFIGURATION2,
)

DEFAULT_CONFIG = {
    SOURCES: SOURCES_CONFIGURATION,
    COMMANDS: BOOLEAN_COMMANDS_CONFIGURATION,
    CONTEXTS: CONTEXTS_CONFIGURATION,
}

STATUE_CONFIGURATION = {
    SOURCES: SOURCES_CONFIGURATION2,
    COMMANDS: OVERRIDE_COMMANDS_CONFIGURATION,
    CONTEXTS: CONTEXTS_INHERITANCE_CONFIGURATION,
}


@pytest.fixture
def existing_file(monkeypatch):
    path_mock = Mock()
    path_mock.exists.return_value = True
    return path_mock


@pytest.fixture
def non_existing_file(monkeypatch):
    path_mock = Mock()
    path_mock.exists.return_value = False
    return path_mock


@pytest.fixture
def non_existing_default_config(non_existing_file, monkeypatch):
    monkeypatch.setattr(
        "statue.constants.DEFAULT_CONFIGURATION_FILE", non_existing_file
    )
    yield non_existing_file
    Configuration.reset_configuration()


@pytest.fixture
def existing_default_config(existing_file, monkeypatch):
    monkeypatch.setattr("statue.constants.DEFAULT_CONFIGURATION_FILE", existing_file)
    yield existing_file
    Configuration.reset_configuration()


@pytest.fixture
def toml_load_mock(mocker):
    return mocker.patch("toml.load")


@pytest.fixture
def existing_non_empty_default_config(existing_default_config, toml_load_mock):
    toml_load_mock.return_value = DEFAULT_CONFIG
    yield
    Configuration.reset_configuration()


@pytest.fixture
def existing_empty_default_config(existing_default_config, toml_load_mock):
    toml_load_mock.return_value = {}
    yield
    Configuration.reset_configuration()


@pytest.fixture
def direct_set_default_config():
    Configuration.default_configuration = DEFAULT_CONFIG
    yield
    Configuration.reset_configuration()


@pytest.fixture
def existing_non_empty_statue_config(toml_load_mock):
    toml_load_mock.return_value = deepcopy(STATUE_CONFIGURATION)
    yield
    Configuration.reset_configuration()


@pytest.fixture
def existing_non_empty_statue_config_with_general_override(toml_load_mock):
    configuration = deepcopy(STATUE_CONFIGURATION)
    configuration[STATUE] = {OVERRIDE: True}
    toml_load_mock.return_value = configuration
    yield
    Configuration.reset_configuration()
