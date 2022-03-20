import os
from pathlib import Path

import mock
import pytest

from statue.config.commands_repository import CommandsRepository
from statue.config.configuration import Configuration
from statue.config.configuration_builder import ConfigurationBuilder
from statue.config.contexts_repository import ContextsRepository
from statue.config.sources_repository import SourcesRepository
from statue.evaluation import Evaluation

# 3rd Party Mocks
from tests.constants import ENVIRON


@pytest.fixture
def mock_time(mocker):
    return mocker.patch("time.time")


@pytest.fixture
def mock_toml_load(mocker):
    return mocker.patch("toml.load")


@pytest.fixture
def mock_toml_dump(mocker):
    return mocker.patch("toml.dump")


@pytest.fixture
def mock_subprocess(mocker):
    return mocker.patch("subprocess.run")


@pytest.fixture
def environ(monkeypatch):
    monkeypatch.setattr(os, "environ", ENVIRON)
    return ENVIRON


# Configuration Mocks


@pytest.fixture
def mock_update_from_config(mocker):
    return mocker.patch.object(ConfigurationBuilder, "update_from_config")


@pytest.fixture
def mock_default_configuration_path(mocker, tmp_path):
    default_path = tmp_path / "default"
    default_path_mock = mocker.patch.object(
        ConfigurationBuilder, "default_configuration_path"
    )
    default_path_mock.return_value = default_path
    return default_path


@pytest.fixture
def mock_configuration_path(mocker, tmp_path):
    dummy_path = tmp_path / "bla.toml"
    configuration_path_mock = mocker.patch.object(
        ConfigurationBuilder, "configuration_path"
    )
    configuration_path_mock.return_value = dummy_path
    return configuration_path_mock


@pytest.fixture
def mock_cache_path(mocker, tmp_path):
    return mocker.patch.object(ConfigurationBuilder, "cache_path")


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
def mock_contexts_repository_as_dict(mocker):
    return mocker.patch.object(ContextsRepository, "as_dict")


@pytest.fixture
def mock_commands_repository_as_dict(mocker):
    return mocker.patch.object(CommandsRepository, "as_dict")


@pytest.fixture
def mock_sources_repository_as_dict(mocker):
    return mocker.patch.object(SourcesRepository, "as_dict")


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
