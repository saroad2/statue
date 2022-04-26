import random
from unittest import mock

import pytest
from pytest_cases import parametrize

from statue.config.commands_repository import CommandsRepository
from statue.config.configuration import Configuration
from statue.config.contexts_repository import ContextsRepository
from statue.config.sources_repository import SourcesRepository
from statue.constants import (
    COMMANDS,
    CONTEXTS,
    DEFAULT_HISTORY_SIZE,
    GENERAL,
    HISTORY_SIZE,
    MODE,
    SOURCES,
)
from statue.exceptions import InvalidConfiguration, StatueConfigurationError
from statue.runner import RunnerMode
from tests.constants import COMMAND1, CONTEXT1


@pytest.fixture
def mock_contexts_repository_from_dict(mocker):
    return mocker.patch.object(ContextsRepository, "from_dict")


@pytest.fixture
def mock_commands_repository_from_dict(mocker):
    return mocker.patch.object(CommandsRepository, "from_dict")


def test_configuration_builder_from_empty_config(tmp_path):
    cache_dir = tmp_path / ".statue"
    configuration = Configuration.from_dict(cache_dir=cache_dir, statue_config_dict={})

    assert isinstance(configuration, Configuration)
    assert len(configuration.contexts_repository) == 0
    assert len(configuration.commands_repository) == 0
    assert len(configuration.sources_repository) == 0
    assert configuration.cache.cache_root_directory == cache_dir
    assert configuration.cache.history_size == DEFAULT_HISTORY_SIZE
    assert configuration.default_mode == RunnerMode.SYNC


@parametrize(argnames="mode", argvalues=[RunnerMode.SYNC, RunnerMode.ASYNC])
def test_configuration_from_dict_mode_upper_case(mode, tmp_path):
    cache_dir = tmp_path / ".statue"
    configuration = Configuration.from_dict(
        cache_dir=cache_dir, statue_config_dict={GENERAL: {MODE: mode.name.upper()}}
    )

    assert len(configuration.contexts_repository) == 0
    assert len(configuration.commands_repository) == 0
    assert len(configuration.sources_repository) == 0
    assert configuration.cache.cache_root_directory == cache_dir
    assert configuration.cache.history_size == DEFAULT_HISTORY_SIZE
    assert configuration.default_mode == mode


@parametrize(argnames="mode", argvalues=[RunnerMode.SYNC, RunnerMode.ASYNC])
def test_configuration_from_dict_mode_lower_case(mode, tmp_path):
    cache_dir = tmp_path / ".statue"
    configuration = Configuration.from_dict(
        cache_dir=cache_dir, statue_config_dict={GENERAL: {MODE: mode.name.lower()}}
    )

    assert len(configuration.contexts_repository) == 0
    assert len(configuration.commands_repository) == 0
    assert len(configuration.sources_repository) == 0
    assert configuration.cache.cache_root_directory == cache_dir
    assert configuration.cache.history_size == DEFAULT_HISTORY_SIZE
    assert configuration.default_mode == mode


def test_configuration_from_dict_history_size(tmp_path):
    cache_dir = tmp_path / ".statue"
    size = random.randint(1, 100)
    configuration = Configuration.from_dict(
        cache_dir=cache_dir, statue_config_dict={GENERAL: {HISTORY_SIZE: size}}
    )

    assert len(configuration.contexts_repository) == 0
    assert len(configuration.commands_repository) == 0
    assert len(configuration.sources_repository) == 0
    assert configuration.cache.cache_root_directory == cache_dir
    assert configuration.cache.history_size == size
    assert configuration.default_mode == RunnerMode.SYNC


def test_configuration_from_dict_update_contexts(
    tmp_path, mock_contexts_repository_from_dict
):
    contexts_config = mock.Mock()
    cache_dir = tmp_path / ".statue"

    configuration = Configuration.from_dict(
        cache_dir=cache_dir, statue_config_dict={CONTEXTS: contexts_config}
    )
    mock_contexts_repository_from_dict.assert_called_once_with(contexts_config)

    contexts_repository = mock_contexts_repository_from_dict.return_value
    assert configuration.contexts_repository == contexts_repository
    assert len(configuration.commands_repository) == 0
    assert len(configuration.sources_repository) == 0
    assert configuration.cache.cache_root_directory == cache_dir
    assert configuration.cache.history_size == DEFAULT_HISTORY_SIZE
    assert configuration.default_mode == RunnerMode.SYNC


def test_configuration_from_dict_update_commands(
    tmp_path, mock_commands_repository_from_dict
):
    commands_config = mock.Mock()
    cache_dir = tmp_path / ".statue"

    configuration = Configuration.from_dict(
        cache_dir=cache_dir, statue_config_dict={COMMANDS: commands_config}
    )
    mock_commands_repository_from_dict.assert_called_once_with(
        config=commands_config,
        contexts_repository=configuration.contexts_repository,
    )

    commands_repository = mock_commands_repository_from_dict.return_value
    assert configuration.commands_repository == commands_repository

    assert len(configuration.contexts_repository) == 0
    assert len(configuration.sources_repository) == 0
    assert configuration.cache.cache_root_directory == cache_dir
    assert configuration.cache.history_size == DEFAULT_HISTORY_SIZE
    assert configuration.default_mode == RunnerMode.SYNC


def test_configuration_from_dict_update_sources(tmp_path):
    sources_config = mock.Mock()
    cache_dir = tmp_path / ".statue"

    with mock.patch.object(SourcesRepository, "from_dict") as sources_from_dict_mock:
        configuration = Configuration.from_dict(
            cache_dir=cache_dir, statue_config_dict={SOURCES: sources_config}
        )
        sources_from_dict_mock.assert_called_once_with(
            config=sources_config, contexts_repository=configuration.contexts_repository
        )

    assert len(configuration.contexts_repository) == 0
    assert len(configuration.commands_repository) == 0
    assert len(configuration.sources_repository) == 0
    assert configuration.cache.cache_root_directory == cache_dir
    assert configuration.cache.history_size == DEFAULT_HISTORY_SIZE
    assert configuration.default_mode == RunnerMode.SYNC


def test_configuration_from_dict_fail_update_mode(tmp_path):
    cache_dir = tmp_path / ".statue"
    with pytest.raises(
        InvalidConfiguration, match=rf"^Got unexpected runner mode BLA \({GENERAL}\)$"
    ):
        Configuration.from_dict(
            cache_dir=cache_dir, statue_config_dict={GENERAL: {MODE: "bla"}}
        )


def test_configuration_from_dict_fail_building_contexts_repository(
    tmp_path, mock_contexts_repository_from_dict
):
    error_message = "Contexts configuration is invalid"
    cache_dir = tmp_path / ".statue"
    contexts_config = mock.Mock()
    mock_contexts_repository_from_dict.side_effect = StatueConfigurationError(
        error_message, location=[CONTEXT1]
    )

    with pytest.raises(
        StatueConfigurationError,
        match=rf"^{error_message} \({CONTEXTS} -> {CONTEXT1}\)$",
    ):
        Configuration.from_dict(
            cache_dir=cache_dir, statue_config_dict={CONTEXTS: contexts_config}
        )

    mock_contexts_repository_from_dict.assert_called_once_with(contexts_config)


def test_configuration_from_dict_fail_building_commands_repository(
    tmp_path, mock_contexts_repository_from_dict, mock_commands_repository_from_dict
):
    error_message = "Commands configuration is invalid"
    cache_dir = tmp_path / ".statue"
    contexts_config, commands_config = mock.Mock(), mock.Mock()
    mock_commands_repository_from_dict.side_effect = StatueConfigurationError(
        error_message, location=[COMMAND1]
    )

    with pytest.raises(
        StatueConfigurationError,
        match=rf"^{error_message} \({COMMANDS} -> {COMMAND1}\)$",
    ):
        Configuration.from_dict(
            cache_dir=cache_dir,
            statue_config_dict={CONTEXTS: contexts_config, COMMANDS: commands_config},
        )

    mock_contexts_repository_from_dict.assert_called_once_with(contexts_config)
    mock_commands_repository_from_dict.assert_called_once_with(
        config=commands_config,
        contexts_repository=mock_contexts_repository_from_dict.return_value,
    )
