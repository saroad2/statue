import asyncio
from pathlib import Path

import pytest
import toml

from statue.cache import Cache
from statue.configuration import Configuration
from statue.constants import OVERRIDE, STATUE
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
def clear_configuration():
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
def mock_sources_list(mocker):
    return mocker.patch.object(Configuration, "sources_list")


@pytest.fixture
def mock_default_configuration(mocker, clear_configuration):
    return mocker.patch.object(Configuration, "default_configuration")


@pytest.fixture
def mock_sources_configuration(mocker, clear_configuration):
    return mocker.patch.object(Configuration, "sources_configuration")


@pytest.fixture
def mock_load_configuration(mocker, clear_configuration):
    return mocker.patch.object(Configuration, "load_configuration")


@pytest.fixture
def mock_cwd(mocker, tmpdir_factory):
    cwd = Path(tmpdir_factory.mktemp("bla"))
    cwd_method_mock = mocker.patch.object(Path, "cwd")
    cwd_method_mock.return_value = cwd
    return cwd


@pytest.fixture
def empty_configuration(mock_cwd, clear_configuration):
    configuration = {
        STATUE: {OVERRIDE: True},
    }
    with open(
        mock_cwd / "statue.toml",
        mode="w",
        encoding="utf-8",
    ) as configuration_file:
        toml.dump(configuration, configuration_file)
    return configuration


# Cache Mocks


@pytest.fixture
def mock_cache_save_evaluation(mocker):
    return mocker.patch.object(Cache, "save_evaluation")


@pytest.fixture
def mock_cache_evaluation_path(mocker):
    return mocker.patch.object(Cache, "evaluation_path")


@pytest.fixture
def mock_cache_all_evaluation_paths(mocker):
    return mocker.patch.object(Cache, "all_evaluation_paths")


@pytest.fixture
def mock_cache_recent_evaluation_path(mocker):
    return mocker.patch.object(Cache, "recent_evaluation_path")


@pytest.fixture
def mock_cache_extract_time_stamp_from_path(mocker):
    return mocker.patch.object(Cache, "extract_time_stamp_from_path")


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
