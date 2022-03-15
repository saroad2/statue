import pytest

from statue.config.commands_repository import CommandsRepository
from statue.config.configuration import Configuration
from statue.config.contexts_repository import ContextsRepository
from statue.config.sources_repository import SourcesRepository
from statue.constants import COMMANDS, CONTEXTS, GENERAL, HISTORY_SIZE, MODE, SOURCES
from statue.runner import RunnerMode


@pytest.fixture
def mock_contexts_repository_as_dict(mocker):
    return mocker.patch.object(ContextsRepository, "as_dict")


@pytest.fixture
def mock_commands_repository_as_dict(mocker):
    return mocker.patch.object(CommandsRepository, "as_dict")


@pytest.fixture
def mock_sources_repository_as_dict(mocker):
    return mocker.patch.object(SourcesRepository, "as_dict")


def test_configuration_default_constructor(
    mock_contexts_repository_as_dict,
    mock_commands_repository_as_dict,
    mock_sources_repository_as_dict,
):
    configuration = Configuration()

    assert configuration.cache.cache_root_directory is None
    assert configuration.cache.history_size == HISTORY_SIZE
    assert len(configuration.commands_repository) == 0
    assert len(configuration.contexts_repository) == 0
    assert len(configuration.sources_repository) == 0
    assert configuration.default_mode == RunnerMode.SYNC
    assert configuration.as_dict() == {
        GENERAL: {MODE: "sync"},
        CONTEXTS: mock_contexts_repository_as_dict.return_value,
        COMMANDS: mock_commands_repository_as_dict.return_value,
        SOURCES: mock_sources_repository_as_dict.return_value,
    }


def test_configuration_constructor_with_cache_dir(
    mock_contexts_repository_as_dict,
    mock_commands_repository_as_dict,
    mock_sources_repository_as_dict,
    tmp_path,
):
    cache_dir = tmp_path / "cache"
    configuration = Configuration(cache_root_directory=cache_dir)

    assert configuration.cache.cache_root_directory == cache_dir
    assert configuration.cache.history_size == HISTORY_SIZE
    assert len(configuration.commands_repository) == 0
    assert len(configuration.contexts_repository) == 0
    assert len(configuration.sources_repository) == 0
    assert configuration.default_mode == RunnerMode.SYNC
    assert configuration.as_dict() == {
        GENERAL: {MODE: "sync"},
        CONTEXTS: mock_contexts_repository_as_dict.return_value,
        COMMANDS: mock_commands_repository_as_dict.return_value,
        SOURCES: mock_sources_repository_as_dict.return_value,
    }


def test_configuration_with_sync_default_mode(
    mock_contexts_repository_as_dict,
    mock_commands_repository_as_dict,
    mock_sources_repository_as_dict,
):
    configuration = Configuration(default_mode=RunnerMode.SYNC)

    assert configuration.cache.cache_root_directory is None
    assert configuration.cache.history_size == HISTORY_SIZE
    assert len(configuration.commands_repository) == 0
    assert len(configuration.contexts_repository) == 0
    assert len(configuration.sources_repository) == 0
    assert configuration.default_mode == RunnerMode.SYNC
    assert configuration.as_dict() == {
        GENERAL: {MODE: "sync"},
        CONTEXTS: mock_contexts_repository_as_dict.return_value,
        COMMANDS: mock_commands_repository_as_dict.return_value,
        SOURCES: mock_sources_repository_as_dict.return_value,
    }


def test_configuration_with_async_default_mode(
    mock_contexts_repository_as_dict,
    mock_commands_repository_as_dict,
    mock_sources_repository_as_dict,
):
    configuration = Configuration(default_mode=RunnerMode.ASYNC)

    assert configuration.cache.cache_root_directory is None
    assert configuration.cache.history_size == HISTORY_SIZE
    assert len(configuration.commands_repository) == 0
    assert len(configuration.contexts_repository) == 0
    assert len(configuration.sources_repository) == 0
    assert configuration.default_mode == RunnerMode.ASYNC
    assert configuration.as_dict() == {
        GENERAL: {MODE: "async"},
        CONTEXTS: mock_contexts_repository_as_dict.return_value,
        COMMANDS: mock_commands_repository_as_dict.return_value,
        SOURCES: mock_sources_repository_as_dict.return_value,
    }
