import asyncio
from pathlib import Path

import mock
import pytest

from statue.config.configuration import Configuration
from statue.config.configuration_builder import ConfigurationBuilder
from statue.evaluation import Evaluation

# 3rd Party Mocks


@pytest.fixture
def mock_time(mocker):
    return mocker.patch("time.time")


@pytest.fixture
def mock_toml_load(mocker):
    return mocker.patch("toml.load")


@pytest.fixture
def mock_toml_dump(mocker):
    return mocker.patch("toml.dump")


# Configuration Mocks


@pytest.fixture
def mock_build_configuration_from_file(mocker):
    builder_mock = mocker.patch.object(
        ConfigurationBuilder, "build_configuration_from_file"
    )
    builder_mock.return_value = Configuration()
    builder_mock.return_value.cache = mock.Mock()
    builder_mock.return_value.build_commands = mock.Mock()
    builder_mock.return_value.build_commands_map = mock.Mock()
    return builder_mock


@pytest.fixture
def mock_cwd(mocker, tmpdir_factory):
    cwd = Path(tmpdir_factory.mktemp("bla"))
    cwd_method_mock = mocker.patch.object(Path, "cwd")
    cwd_method_mock.return_value = cwd
    return cwd


# Evaluation Mocks


@pytest.fixture
def mock_evaluation_load_from_file(mocker):
    return mocker.patch.object(Evaluation, "load_from_file")


@pytest.fixture
def mock_evaluation_save_as_json(mocker):
    return mocker.patch.object(Evaluation, "save_as_json")


# Built-in Mocks


@pytest.fixture
def print_mock(mocker):
    return mocker.patch("builtins.print")


@pytest.fixture
def reset_events_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
