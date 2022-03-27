from pathlib import Path
from unittest.mock import Mock, call

import pytest

from statue.commands_filter import CommandsFilter
from statue.commands_map import CommandsMap
from statue.config.configuration import Configuration
from statue.context import Context
from tests.constants import (
    COMMAND1,
    COMMAND2,
    COMMAND3,
    CONTEXT1,
    CONTEXT2,
    CONTEXT_HELP_STRING1,
    CONTEXT_HELP_STRING2,
    SOURCE1,
    SOURCE2,
)
from tests.util import assert_calls


def assert_commands_count(commands_map, count):
    assert (
        commands_map.total_commands_count == count
    ), "Commands count is different than expected"


def assert_sources(commands_map, sources):
    assert (
        list(commands_map.keys()) == sources
    ), "Commands map doesn't include all sources"


def assert_commands(commands_map, source, commands):
    assert (
        commands_map[source] == commands
    ), f"Commands of {source} are different than expected"


@pytest.fixture
def mock_build_commands(mocker):
    return mocker.patch.object(Configuration, "build_commands")


def test_get_commands_map_source_from_config(mock_build_commands):
    command = Mock()
    context = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    configuration = Configuration()
    configuration.contexts_repository.add_contexts(context)
    configuration.sources_repository[Path(SOURCE1)] = CommandsFilter(
        allowed_commands=[COMMAND1], contexts=[context]
    )
    mock_build_commands.return_value = [command]
    commands_map = configuration.build_commands_map(
        sources=[Path(SOURCE1)], commands_filter=CommandsFilter()
    )
    assert_commands_count(commands_map, 1)
    assert_sources(commands_map, [Path(SOURCE1)])
    assert_commands(commands_map, Path(SOURCE1), [command])
    assert_calls(
        mock_build_commands,
        [
            call(
                CommandsFilter(
                    allowed_commands=[COMMAND1],
                    contexts=[context],
                )
            )
        ],
    )


def test_get_commands_map_source_not_from_config(mock_build_commands):
    command = Mock()
    context = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    configuration = Configuration()
    configuration.contexts_repository.add_contexts(context)
    configuration.sources_repository[Path(SOURCE1)] = CommandsFilter(
        denied_commands=[COMMAND3], contexts=[context]
    )
    mock_build_commands.return_value = [command]
    commands_map = configuration.build_commands_map(
        sources=[Path(SOURCE2)], commands_filter=CommandsFilter()
    )
    assert_commands_count(commands_map, 1)
    assert_sources(commands_map, [Path(SOURCE2)])
    assert_commands(commands_map, Path(SOURCE2), [command])
    assert_calls(
        mock_build_commands,
        [call(CommandsFilter())],
    )


def test_get_commands_map_with_no_commands(mock_build_commands):
    context = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    configuration = Configuration()
    configuration.contexts_repository.add_contexts(context)
    configuration.sources_repository[Path(SOURCE1)] = CommandsFilter()
    configuration.sources_repository[Path(SOURCE2)] = CommandsFilter()
    commands_filter = CommandsFilter(denied_commands=COMMAND3, contexts=[context])
    mock_build_commands.side_effect = lambda _: []
    commands_map = configuration.build_commands_map(
        sources=[Path(SOURCE1), Path(SOURCE2)], commands_filter=commands_filter
    )
    assert commands_map == CommandsMap()
    assert_calls(mock_build_commands, [call(commands_filter), call(commands_filter)])


def test_get_commands_map_with_commands_without_directives(mock_build_commands):
    command1, command2, command3 = Mock(), Mock(), Mock()
    configuration = Configuration()
    configuration.sources_repository[Path(SOURCE1)] = CommandsFilter()
    configuration.sources_repository[Path(SOURCE2)] = CommandsFilter()
    mock_build_commands.side_effect = [[command1], [command2, command3]]
    commands_map = configuration.build_commands_map(
        sources=[Path(SOURCE1), Path(SOURCE2)], commands_filter=CommandsFilter()
    )
    assert_commands_count(commands_map, 3)
    assert_sources(commands_map, [Path(SOURCE1), Path(SOURCE2)])
    assert_commands(commands_map, Path(SOURCE1), [command1])
    assert_commands(commands_map, Path(SOURCE2), [command2, command3])
    assert_calls(
        mock_build_commands,
        [call(CommandsFilter()), call(CommandsFilter())],
    )


def test_get_commands_map_with_commands_and_directives(mock_build_commands):
    command1, command2, command3 = Mock(), Mock(), Mock()
    context = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    configuration = Configuration()
    configuration.contexts_repository.add_contexts(context)
    configuration.sources_repository[Path(SOURCE1)] = CommandsFilter()
    configuration.sources_repository[Path(SOURCE2)] = CommandsFilter()
    commands_filter = CommandsFilter(allowed_commands=[COMMAND1], contexts=[context])
    mock_build_commands.side_effect = [[command1], [command2, command3]]
    commands_map = configuration.build_commands_map(
        sources=[Path(SOURCE1), Path(SOURCE2)], commands_filter=commands_filter
    )
    assert_commands_count(commands_map, 3)
    assert_sources(commands_map, [Path(SOURCE1), Path(SOURCE2)])
    assert_commands(commands_map, Path(SOURCE1), [command1])
    assert_commands(commands_map, Path(SOURCE2), [command2, command3])
    assert_calls(mock_build_commands, [call(commands_filter), call(commands_filter)])


def test_get_commands_map_with_source_context(mock_build_commands):
    command1, command2, command3 = Mock(), Mock(), Mock()
    context1, context2 = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1), Context(
        name=CONTEXT2, help=CONTEXT_HELP_STRING2
    )
    configuration = Configuration()
    configuration.contexts_repository.add_contexts(context1, context2)
    configuration.sources_repository[Path(SOURCE1)] = CommandsFilter(
        contexts=[context1]
    )
    configuration.sources_repository[Path(SOURCE2)] = CommandsFilter()
    mock_build_commands.side_effect = [[command1, command2], [command3]]
    commands_map = configuration.build_commands_map(
        sources=[Path(SOURCE1), Path(SOURCE2)],
        commands_filter=CommandsFilter(denied_commands=[COMMAND3], contexts=[context2]),
    )
    assert_commands_count(commands_map, 3)
    assert_sources(commands_map, [Path(SOURCE1), Path(SOURCE2)])
    assert_commands(commands_map, Path(SOURCE1), [command1, command2])
    assert_commands(commands_map, Path(SOURCE2), [command3])
    assert_calls(
        mock_build_commands,
        [
            call(
                CommandsFilter(
                    denied_commands=[COMMAND3],
                    contexts=[context1, context2],
                )
            ),
            call(
                CommandsFilter(
                    denied_commands=[COMMAND3],
                    contexts=[context2],
                )
            ),
        ],
    )


def test_get_commands_map_with_source_allow_list(mock_build_commands):
    command1, command2 = Mock(), Mock()
    mock_build_commands.side_effect = [[command1], [command2]]
    configuration = Configuration()
    configuration.contexts_repository.add_contexts(
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    )
    configuration.sources_repository[Path(SOURCE1)] = CommandsFilter()
    configuration.sources_repository[Path(SOURCE2)] = CommandsFilter(
        allowed_commands=[COMMAND2]
    )
    commands_map = configuration.build_commands_map(
        sources=[Path(SOURCE1), Path(SOURCE2)],
        commands_filter=CommandsFilter(
            allowed_commands=[COMMAND1, COMMAND2], contexts=[CONTEXT1]
        ),
    )
    assert_commands_count(commands_map, 2)
    assert_sources(commands_map, [Path(SOURCE1), Path(SOURCE2)])
    assert_commands(commands_map, Path(SOURCE1), [command1])
    assert_commands(commands_map, Path(SOURCE2), [command2])
    assert_calls(
        mock_build_commands,
        [
            call(
                CommandsFilter(
                    allowed_commands=[COMMAND1, COMMAND2], contexts=[CONTEXT1]
                )
            ),
            call(CommandsFilter(allowed_commands=[COMMAND2], contexts=[CONTEXT1])),
        ],
    )


def test_get_commands_map_with_source_deny_list(mock_build_commands):
    command1, command2, command3, command4 = (
        Mock(),
        Mock(),
        Mock(),
        Mock(),
    )
    mock_build_commands.side_effect = [[command1, command2], [command3, command4]]
    context = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    configuration = Configuration()
    configuration.contexts_repository.add_contexts(context)
    configuration.sources_repository[Path(SOURCE1)] = CommandsFilter()
    configuration.sources_repository[Path(SOURCE2)] = CommandsFilter(
        denied_commands=[COMMAND2]
    )
    commands_map = configuration.build_commands_map(
        sources=[Path(SOURCE1), Path(SOURCE2)],
        commands_filter=CommandsFilter(denied_commands=[COMMAND3], contexts=[context]),
    )
    assert_commands_count(commands_map, 4)
    assert_sources(commands_map, [Path(SOURCE1), Path(SOURCE2)])
    assert_commands(commands_map, Path(SOURCE1), [command1, command2])
    assert_commands(commands_map, Path(SOURCE2), [command3, command4])
    assert_calls(
        mock_build_commands,
        [
            call(CommandsFilter(denied_commands=[COMMAND3], contexts=[context])),
            call(
                CommandsFilter(denied_commands=[COMMAND3, COMMAND2], contexts=[context])
            ),
        ],
    )


def test_get_commands_map_from_relative_path(mock_build_commands):
    command1, command2 = (Mock(), Mock())
    context1, context2 = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1), Context(
        name=CONTEXT2, help=CONTEXT_HELP_STRING2
    )
    configuration = Configuration()
    configuration.contexts_repository.add_contexts(context1, context2)
    configuration.sources_repository[Path(SOURCE1)] = CommandsFilter(
        contexts=[context1]
    )
    configuration.sources_repository[Path(SOURCE2)] = CommandsFilter(
        contexts=[context2]
    )
    mock_build_commands.side_effect = [[command1, command2]]
    relative_source = Path(SOURCE2) / "i" / "am" / "relative"

    commands_map = configuration.build_commands_map(
        sources=[relative_source], commands_filter=CommandsFilter()
    )

    assert_sources(commands_map, [relative_source])
    assert_commands(commands_map, relative_source, [command1, command2])
    assert_commands_count(commands_map, 2)
    assert_calls(
        mock_build_commands,
        [
            call(
                CommandsFilter(
                    contexts=[context2], allowed_commands=None, denied_commands=None
                )
            )
        ],
    )
