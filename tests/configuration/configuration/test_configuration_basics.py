import mock

from statue.config.configuration import Configuration
from statue.runner import RunnerMode


def test_configuration_constructor_without_mode(tmp_path):
    cache = mock.Mock()
    configuration = Configuration(cache=cache)

    assert configuration.cache == cache
    assert len(configuration.commands_repository) == 0
    assert len(configuration.contexts_repository) == 0
    assert len(configuration.sources_repository) == 0
    assert configuration.default_mode == RunnerMode.SYNC


def test_configuration_with_sync_default_mode():
    cache = mock.Mock()
    configuration = Configuration(cache=cache, default_mode=RunnerMode.SYNC)

    assert configuration.cache == cache
    assert len(configuration.commands_repository) == 0
    assert len(configuration.contexts_repository) == 0
    assert len(configuration.sources_repository) == 0
    assert configuration.default_mode == RunnerMode.SYNC


def test_configuration_with_async_default_mode():
    cache = mock.Mock()
    configuration = Configuration(cache=cache, default_mode=RunnerMode.ASYNC)

    assert configuration.cache == cache
    assert len(configuration.commands_repository) == 0
    assert len(configuration.contexts_repository) == 0
    assert len(configuration.sources_repository) == 0
    assert configuration.default_mode == RunnerMode.ASYNC
