import os
import random
from pathlib import Path

import mock
import pytest

from statue.cache import Cache
from statue.config.commands_repository import CommandsRepository
from statue.config.configuration import Configuration
from statue.config.contexts_repository import ContextsRepository
from statue.config.sources_repository import SourcesRepository
from statue.constants import DEFAULT_HISTORY_SIZE
from statue.evaluation import Evaluation
from statue.templates.templates_provider import TemplatesProvider
from tests.constants import ENVIRON

# 3rd Party Mocks


@pytest.fixture
def mock_time(mocker):
    return mocker.patch("time.time")


@pytest.fixture
def mock_toml_load(mocker):
    return mocker.patch("tomli.load")


@pytest.fixture
def mock_tqdm(mocker):
    return mocker.patch("tqdm.tqdm")


@pytest.fixture
def mock_tqdm_range(mocker):
    return mocker.patch("tqdm.trange")


# Configuration Mocks


@pytest.fixture
def empty_configuration(tmp_path):
    cache_dir = tmp_path / "cache"
    cache = Cache(size=DEFAULT_HISTORY_SIZE, cache_root_directory=cache_dir)
    return Configuration(cache)


@pytest.fixture
def mock_configuration_path(mocker, tmp_path):
    dummy_path = tmp_path / "bla.toml"
    configuration_path_mock = mocker.patch.object(Configuration, "configuration_path")
    configuration_path_mock.return_value = dummy_path
    return configuration_path_mock


@pytest.fixture
def mock_cache_path(mocker, tmp_path):
    return mocker.patch.object(Configuration, "cache_path")


@pytest.fixture
def mock_build_configuration_from_file(mocker):
    history_size = random.randint(1, 100)
    builder_mock = mocker.patch.object(Configuration, "from_file")
    builder_mock.return_value = Configuration(cache=Cache(size=history_size))
    builder_mock.return_value.cache = mock.Mock()
    builder_mock.return_value.build_commands = mock.Mock()
    builder_mock.return_value.build_commands_map = mock.Mock()
    builder_mock.return_value.to_toml = mock.Mock()
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
def mock_configuration_as_dict(mocker):
    return mocker.patch.object(Configuration, "as_dict")


@pytest.fixture
def mock_cwd(mocker, tmpdir_factory):
    cwd = Path(tmpdir_factory.mktemp("bla"))
    cwd_method_mock = mocker.patch.object(Path, "cwd")
    cwd_method_mock.return_value = cwd
    return cwd


@pytest.fixture
def mock_home(mocker, tmpdir_factory):
    home = Path(tmpdir_factory.mktemp("bla"))
    home_method_mock = mocker.patch.object(Path, "home")
    home_method_mock.return_value = home
    return home


# Templates Provider Mocks


@pytest.fixture()
def mock_templates_provider_default_names(mocker):
    return mocker.patch.object(TemplatesProvider, "default_templates_names")


@pytest.fixture()
def mock_templates_provider_user_names(mocker):
    return mocker.patch.object(TemplatesProvider, "user_templates_names")


@pytest.fixture()
def mock_templates_provider_get_template_path(mocker):
    return mocker.patch.object(TemplatesProvider, "get_template_path")


@pytest.fixture()
def mock_templates_provider_save_template(mocker):
    return mocker.patch.object(TemplatesProvider, "save_template")


@pytest.fixture()
def mock_templates_provider_remove_template(mocker):
    return mocker.patch.object(TemplatesProvider, "remove_template")


@pytest.fixture()
def mock_templates_provider_clear_user_templates(mocker):
    return mocker.patch.object(TemplatesProvider, "clear_user_templates")


# Evaluation Mocks


@pytest.fixture
def mock_evaluation_load_from_file(mocker):
    return mocker.patch.object(Evaluation, "load_from_file")


# Built-in Mocks


@pytest.fixture
def print_mock(mocker):
    return mocker.patch("builtins.print")


@pytest.fixture
def mock_subprocess(mocker):
    return mocker.patch("subprocess.run")


@pytest.fixture
def environ(monkeypatch):
    monkeypatch.setattr(os, "environ", ENVIRON)
    return ENVIRON
