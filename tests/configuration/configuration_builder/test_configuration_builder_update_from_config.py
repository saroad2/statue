from unittest import mock

import pytest
from pytest_cases import parametrize

from statue.config.configuration import Configuration
from statue.config.configuration_builder import ConfigurationBuilder
from statue.constants import COMMANDS, CONTEXTS, GENERAL, MODE, SOURCES
from statue.exceptions import InvalidConfiguration
from statue.runner import RunnerMode


def test_configuration_builder_update_from_empty_config():
    configuration = Configuration()

    ConfigurationBuilder.update_from_config(
        configuration=configuration, statue_config={}
    )

    assert len(configuration.contexts_repository) == 0
    assert len(configuration.commands_repository) == 0
    assert len(configuration.sources_repository) == 0
    assert configuration.default_mode == RunnerMode.SYNC


@parametrize(argnames="mode", argvalues=[RunnerMode.SYNC, RunnerMode.ASYNC])
def test_configuration_builder_update_mode_upper_case(mode):
    configuration = Configuration()

    ConfigurationBuilder.update_from_config(
        configuration=configuration, statue_config={GENERAL: {MODE: mode.name.upper()}}
    )

    assert len(configuration.contexts_repository) == 0
    assert len(configuration.commands_repository) == 0
    assert len(configuration.sources_repository) == 0
    assert configuration.default_mode == mode


@parametrize(argnames="mode", argvalues=[RunnerMode.SYNC, RunnerMode.ASYNC])
def test_configuration_builder_update_mode_lower_case(mode):
    configuration = Configuration()

    ConfigurationBuilder.update_from_config(
        configuration=configuration, statue_config={GENERAL: {MODE: mode.name.lower()}}
    )

    assert len(configuration.contexts_repository) == 0
    assert len(configuration.commands_repository) == 0
    assert len(configuration.sources_repository) == 0
    assert configuration.default_mode == mode


def test_configuration_builder_update_contexts():
    configuration = Configuration()
    contexts_config = mock.Mock()

    with mock.patch.object(
        configuration.contexts_repository, "update_from_config"
    ) as contexts_update_mock:
        ConfigurationBuilder.update_from_config(
            configuration=configuration, statue_config={CONTEXTS: contexts_config}
        )
        contexts_update_mock.assert_called_once_with(contexts_config)

    assert len(configuration.contexts_repository) == 0
    assert len(configuration.commands_repository) == 0
    assert len(configuration.sources_repository) == 0
    assert configuration.default_mode == RunnerMode.SYNC


def test_configuration_builder_update_commands():
    configuration = Configuration()
    commands_config = mock.Mock()

    with mock.patch.object(
        configuration.commands_repository, "update_from_config"
    ) as commands_update_mock:
        ConfigurationBuilder.update_from_config(
            configuration=configuration, statue_config={COMMANDS: commands_config}
        )
        commands_update_mock.assert_called_once_with(commands_config)

    assert len(configuration.contexts_repository) == 0
    assert len(configuration.commands_repository) == 0
    assert len(configuration.sources_repository) == 0
    assert configuration.default_mode == RunnerMode.SYNC


def test_configuration_builder_update_sources():
    configuration = Configuration()
    sources_config = mock.Mock()

    with mock.patch.object(
        configuration.sources_repository, "update_from_config"
    ) as sources_update_mock:
        ConfigurationBuilder.update_from_config(
            configuration=configuration, statue_config={SOURCES: sources_config}
        )
        sources_update_mock.assert_called_once_with(
            config=sources_config, contexts_repository=configuration.contexts_repository
        )

    assert len(configuration.contexts_repository) == 0
    assert len(configuration.commands_repository) == 0
    assert len(configuration.sources_repository) == 0
    assert configuration.default_mode == RunnerMode.SYNC


def test_configuration_builder_update_fail_update_mode():
    configuration = Configuration()

    with pytest.raises(
        InvalidConfiguration, match="^Got unexpected runner mode in configuration: BLA$"
    ):
        ConfigurationBuilder.update_from_config(
            configuration=configuration, statue_config={GENERAL: {MODE: "bla"}}
        )
