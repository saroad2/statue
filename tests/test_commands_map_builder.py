import random

import mock
import pytest

from statue.cache import Cache
from statue.commands_filter import CommandsFilter
from statue.commands_map_builder import CommandsMapBuilder
from statue.config.configuration import Configuration
from statue.context import Context
from statue.exceptions import CacheError, CommandsMapBuilderError
from tests.constants import (
    COMMAND1,
    COMMAND2,
    COMMAND3,
    CONTEXT1,
    CONTEXT2,
    CONTEXT3,
    CONTEXT_HELP_STRING1,
    CONTEXT_HELP_STRING2,
    CONTEXT_HELP_STRING3,
    SOURCE1,
    SOURCE2,
    SOURCE3,
)

# Successful tests


def test_commands_map_builder_with_default_settings(tmp_path):
    sources_list = [tmp_path / SOURCE1, tmp_path / SOURCE2, tmp_path / SOURCE3]
    configuration = mock.Mock()
    configuration.sources_repository.sources_list = sources_list
    commands_map_builder = CommandsMapBuilder(configuration=configuration)

    commands_map = commands_map_builder.build()

    assert commands_map == configuration.build_commands_map.return_value
    configuration.build_commands_map.assert_called_once_with(
        sources=sources_list, commands_filter=CommandsFilter()
    )


def test_commands_map_builder_with_specified_sources(tmp_path):
    sources_list = [tmp_path / SOURCE1, tmp_path / SOURCE2, tmp_path / SOURCE3]
    configuration = mock.Mock()
    commands_map_builder = CommandsMapBuilder(
        specified_sources=sources_list, configuration=configuration
    )

    commands_map = commands_map_builder.build()

    assert commands_map == configuration.build_commands_map.return_value
    configuration.build_commands_map.assert_called_once_with(
        sources=sources_list, commands_filter=CommandsFilter()
    )


def test_commands_map_builder_with_allowed_commands(tmp_path):
    sources_list = [tmp_path / SOURCE1, tmp_path / SOURCE2, tmp_path / SOURCE3]
    allowed_commands = [COMMAND1, COMMAND2, COMMAND3]
    configuration = mock.Mock()
    configuration.sources_repository.sources_list = sources_list
    commands_map_builder = CommandsMapBuilder(
        specified_sources=sources_list,
        configuration=configuration,
        allowed_commands=allowed_commands,
    )

    commands_map = commands_map_builder.build()

    assert commands_map == configuration.build_commands_map.return_value
    configuration.build_commands_map.assert_called_once_with(
        sources=sources_list,
        commands_filter=CommandsFilter(allowed_commands=allowed_commands),
    )


def test_commands_map_builder_with_denied_commands(tmp_path):
    sources_list = [tmp_path / SOURCE1, tmp_path / SOURCE2, tmp_path / SOURCE3]
    denied_commands = [COMMAND1, COMMAND2, COMMAND3]
    configuration = mock.Mock()
    configuration.sources_repository.sources_list = sources_list
    commands_map_builder = CommandsMapBuilder(
        specified_sources=sources_list,
        configuration=configuration,
        denied_commands=denied_commands,
    )

    commands_map = commands_map_builder.build()

    assert commands_map == configuration.build_commands_map.return_value
    configuration.build_commands_map.assert_called_once_with(
        sources=sources_list,
        commands_filter=CommandsFilter(denied_commands=denied_commands),
    )


def test_commands_map_builder_with_contexts(tmp_path):
    sources_list = [tmp_path / SOURCE1, tmp_path / SOURCE2, tmp_path / SOURCE3]
    contexts = [
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1),
        Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2),
        Context(name=CONTEXT3, help=CONTEXT_HELP_STRING3),
    ]
    configuration = mock.Mock()
    configuration.sources_repository.sources_list = sources_list
    commands_map_builder = CommandsMapBuilder(
        specified_sources=sources_list, configuration=configuration, contexts=contexts
    )

    commands_map = commands_map_builder.build()

    assert commands_map == configuration.build_commands_map.return_value
    configuration.build_commands_map.assert_called_once_with(
        sources=sources_list, commands_filter=CommandsFilter(contexts=contexts)
    )


def test_commands_map_builder_on_previous_evaluation():
    previous = 3
    configuration = mock.Mock()
    commands_map_builder = CommandsMapBuilder(
        configuration=configuration, previous=previous
    )

    commands_map = commands_map_builder.build()

    assert commands_map == configuration.cache.get_evaluation.return_value.commands_map
    configuration.cache.get_evaluation.assert_called_once_with(previous - 1)


def test_commands_map_builder_on_failed_evaluation():
    configuration = mock.Mock()
    commands_map_builder = CommandsMapBuilder(configuration=configuration, failed=True)

    commands_map = commands_map_builder.build()

    assert commands_map == configuration.cache.recent_failed_evaluation.commands_map


def test_commands_map_builder_with_failed_only():
    configuration = mock.Mock()
    commands_map_builder = CommandsMapBuilder(
        configuration=configuration, failed_only=True
    )

    commands_map = commands_map_builder.build()

    assert (
        commands_map
        == configuration.cache.recent_failed_evaluation.failure_evaluation.commands_map
    )


def test_commands_map_builder_with_previous_and_failed_only():
    previous = 3
    configuration = mock.Mock()
    commands_map_builder = CommandsMapBuilder(
        configuration=configuration, failed_only=True, previous=previous
    )

    commands_map = commands_map_builder.build()
    expected_commands_map = (
        configuration.cache.get_evaluation.return_value.failure_evaluation.commands_map
    )

    assert commands_map == expected_commands_map
    configuration.cache.get_evaluation.assert_called_once_with(previous - 1)


# Exception tests


def test_commands_map_builder_cannot_be_set_with_both_failed_and_previous():
    commands_map_builder = CommandsMapBuilder(
        configuration=mock.Mock(), previous=random.randint(0, 5), failed=True
    )

    with pytest.raises(
        CommandsMapBuilderError,
        match='^"failed" and "previous" cannot both be set when building commands map$',
    ):
        commands_map_builder.build()


def test_commands_map_builder_fail_due_to_empty_sources(tmp_path):
    configuration = mock.Mock()
    configuration.sources_repository.sources_list = []
    commands_map_builder = CommandsMapBuilder(configuration=configuration)

    with pytest.raises(
        CommandsMapBuilderError,
        match="^No source was specified and no Sources section in configuration.$",
    ):
        commands_map_builder.build()


def test_commands_map_builder_on_previous_evaluation_fails_due_to_cache_error():
    previous = 3
    error_message = "This is a message"
    configuration = mock.Mock()
    commands_map_builder = CommandsMapBuilder(
        configuration=configuration, previous=previous
    )
    configuration.cache.get_evaluation.side_effect = CacheError(error_message)

    with pytest.raises(CommandsMapBuilderError, match=f"^{error_message}$"):
        commands_map_builder.build()

    configuration.cache.get_evaluation.assert_called_once_with(previous - 1)


def test_commands_map_builder_on_failed_evaluation_fails_due_to_cache_error():
    message = "This is a message"
    configuration = Configuration(cache=Cache(10))
    commands_map_builder = CommandsMapBuilder(configuration=configuration, failed=True)
    with mock.patch.object(
        Cache, "recent_failed_evaluation", new_callable=mock.PropertyMock
    ) as recent_failed_evaluation:
        recent_failed_evaluation.side_effect = CacheError(message)
        with pytest.raises(CommandsMapBuilderError, match=f"^{message}$"):
            commands_map_builder.build()


def test_commands_map_builder_on_failed_old_evaluation_fails_due_to_cache_error():
    message = "This is a message"
    configuration = Configuration(cache=Cache(10))
    commands_map_builder = CommandsMapBuilder(
        configuration=configuration, failed_only=True
    )
    with mock.patch.object(
        Cache, "recent_failed_evaluation", new_callable=mock.PropertyMock
    ) as recent_failed_evaluation:
        recent_failed_evaluation.side_effect = CacheError(message)
        with pytest.raises(CommandsMapBuilderError, match=f"^{message}$"):
            commands_map_builder.build()
