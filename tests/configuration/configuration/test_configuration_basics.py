from pytest_cases import parametrize

from statue.config.configuration import Configuration
from statue.constants import HISTORY_SIZE
from statue.runner import RunnerMode


def test_configuration_default_constructor():
    configuration = Configuration()

    assert configuration.cache.cache_root_directory is None
    assert configuration.cache.history_size == HISTORY_SIZE
    assert len(configuration.commands_repository) == 0
    assert len(configuration.contexts_repository) == 0
    assert len(configuration.sources_repository) == 0
    assert configuration.default_mode == RunnerMode.SYNC


def test_configuration_constructor_with_cache_dir(tmp_path):
    cache_dir = tmp_path / "cache"
    configuration = Configuration(cache_root_directory=cache_dir)

    assert configuration.cache.cache_root_directory == cache_dir
    assert configuration.cache.history_size == HISTORY_SIZE
    assert len(configuration.commands_repository) == 0
    assert len(configuration.contexts_repository) == 0
    assert len(configuration.sources_repository) == 0
    assert configuration.default_mode == RunnerMode.SYNC


@parametrize(argnames="mode", argvalues=[RunnerMode.SYNC, RunnerMode.ASYNC])
def test_configuration_with_default_mode(mode):
    configuration = Configuration(default_mode=mode)

    assert configuration.cache.cache_root_directory is None
    assert configuration.cache.history_size == HISTORY_SIZE
    assert len(configuration.commands_repository) == 0
    assert len(configuration.contexts_repository) == 0
    assert len(configuration.sources_repository) == 0
    assert configuration.default_mode == mode
