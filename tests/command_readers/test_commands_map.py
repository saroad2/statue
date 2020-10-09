from unittest.mock import Mock, call

import pytest

from statue.commands_map import read_commands_map
from statue.constants import ALLOW_LIST, CONTEXTS, DENY_LIST, SOURCES
from statue.exceptions import MissingConfiguration
from tests.constants import (
    COMMAND1,
    COMMAND2,
    COMMAND3,
    CONTEXT1,
    CONTEXT2,
    SOURCE1,
    SOURCE2,
)
from tests.util import assert_calls


def assert_sources(commands_map, sources):
    assert (
        list(commands_map.keys()) == sources
    ), "Commands map doesn't include all sources"


def assert_commands(commands_map, source, commands):
    assert (
        commands_map[source] == commands
    ), f"Commands of {source} are different than expected"


def test_get_commands_map_source_from_config(
    mock_read_commands, mock_sources_configuration
):
    command = Mock()
    mock_sources_configuration.return_value = {
        SOURCE1: dict(allow_list=[COMMAND1], deny_list=[COMMAND3], contexts=[CONTEXT2])
    }
    mock_read_commands.return_value = [command]
    commands_map = read_commands_map([SOURCE1])
    assert_sources(commands_map, [SOURCE1])
    assert_commands(commands_map, SOURCE1, [command])
    assert_calls(
        mock_read_commands,
        [call(allow_list=[COMMAND1], deny_list=[COMMAND3], contexts=[CONTEXT2])],
    )


def test_get_commands_map_source_not_from_config(
    mock_read_commands, mock_sources_configuration
):
    command = Mock()
    mock_sources_configuration.return_value = {
        SOURCE1: dict(allow_list=[COMMAND1], deny_list=[COMMAND3], contexts=[CONTEXT2])
    }
    mock_read_commands.return_value = [command]
    commands_map = read_commands_map([SOURCE2])
    assert_sources(commands_map, [SOURCE2])
    assert_commands(commands_map, SOURCE2, [command])
    assert_calls(
        mock_read_commands,
        [call(allow_list=None, deny_list=None, contexts=None)],
    )


def test_get_commands_map_source_with_no_config(
    mock_read_commands, mock_sources_configuration
):
    command = Mock()
    mock_sources_configuration.side_effect = MissingConfiguration(SOURCES)
    mock_read_commands.return_value = [command]
    commands_map = read_commands_map([SOURCE1])
    assert_sources(commands_map, [SOURCE1])
    assert_commands(commands_map, SOURCE1, [command])
    assert_calls(
        mock_read_commands,
        [call(allow_list=None, deny_list=None, contexts=None)],
    )


def test_get_commands_map_with_no_sources(
    mock_sources_configuration, mock_read_commands
):
    mock_sources_configuration.side_effect = MissingConfiguration(SOURCES)
    with pytest.raises(
        MissingConfiguration,
        match=f'^"{SOURCES}" is missing from Statue configuration.$',
    ):
        read_commands_map([])


def test_get_commands_map_with_no_commands(
    mock_sources_configuration, mock_read_commands
):
    kwargs = dict(allow_list=[COMMAND1], deny_list=[COMMAND3], contexts=[CONTEXT2])
    mock_sources_configuration.return_value = {SOURCE1: {}, SOURCE2: {}}
    mock_read_commands.return_value = None
    commands_map = read_commands_map([], **kwargs)
    assert commands_map is None
    assert_calls(mock_read_commands, [call(**kwargs), call(**kwargs)])


def test_get_commands_map_with_commands_without_directives(
    mock_sources_configuration, mock_read_commands
):
    command1, command2, command3 = Mock(), Mock(), Mock()
    mock_sources_configuration.return_value = {SOURCE1: {}, SOURCE2: {}}
    mock_read_commands.side_effect = [[command1], [command2, command3]]
    commands_map = read_commands_map([])
    assert_sources(commands_map, [SOURCE1, SOURCE2])
    assert_commands(commands_map, SOURCE1, [command1])
    assert_commands(commands_map, SOURCE2, [command2, command3])
    assert_calls(
        mock_read_commands,
        [
            call(allow_list=None, contexts=None, deny_list=None),
            call(allow_list=None, contexts=None, deny_list=None),
        ],
    )


def test_get_commands_map_with_commands_and_directives(
    mock_sources_configuration, mock_read_commands
):
    command1, command2, command3 = Mock(), Mock(), Mock()
    kwargs = dict(allow_list=[COMMAND1], deny_list=[COMMAND3], contexts=[CONTEXT2])
    mock_sources_configuration.return_value = {SOURCE1: {}, SOURCE2: {}}
    mock_read_commands.side_effect = [[command1], [command2, command3]]
    commands_map = read_commands_map([], **kwargs)
    assert_sources(commands_map, [SOURCE1, SOURCE2])
    assert_commands(commands_map, SOURCE1, [command1])
    assert_commands(commands_map, SOURCE2, [command2, command3])
    assert_calls(mock_read_commands, [call(**kwargs), call(**kwargs)])


def test_get_commands_map_with_source_context(
    mock_sources_configuration, mock_read_commands
):
    command1, command2, command3 = Mock(), Mock(), Mock()
    kwargs = dict(allow_list=[COMMAND1], deny_list=[COMMAND3], contexts=[CONTEXT2])
    mock_sources_configuration.return_value = {
        SOURCE1: {CONTEXTS: [CONTEXT1]},
        SOURCE2: {},
    }
    mock_read_commands.side_effect = [[command1, command2], [command3]]
    commands_map = read_commands_map([], **kwargs)
    assert_sources(commands_map, [SOURCE1, SOURCE2])
    assert_commands(commands_map, SOURCE1, [command1, command2])
    assert_commands(commands_map, SOURCE2, [command3])
    assert_calls(
        mock_read_commands,
        [
            call(
                allow_list=[COMMAND1],
                deny_list=[COMMAND3],
                contexts=[CONTEXT2, CONTEXT1],
            ),
            call(**kwargs),
        ],
    )


def test_get_commands_map_with_source_allow_list(
    mock_sources_configuration, mock_read_commands
):
    command1, command2 = Mock(), Mock()
    kwargs = dict(
        allow_list=[COMMAND1, COMMAND2], deny_list=[COMMAND3], contexts=[CONTEXT1]
    )
    mock_sources_configuration.return_value = {
        SOURCE1: {},
        SOURCE2: {ALLOW_LIST: [COMMAND2]},
    }
    mock_read_commands.side_effect = [[command1], [command2]]
    commands_map = read_commands_map([], **kwargs)
    assert_sources(commands_map, [SOURCE1, SOURCE2])
    assert_commands(commands_map, SOURCE1, [command1])
    assert_commands(commands_map, SOURCE2, [command2])
    assert_calls(
        mock_read_commands,
        [
            call(**kwargs),
            call(allow_list=[COMMAND2], deny_list=[COMMAND3], contexts=[CONTEXT1]),
        ],
    )


def test_get_commands_map_with_source_deny_list(
    mock_sources_configuration, mock_read_commands
):
    command1, command2, command3, command4 = (
        Mock(),
        Mock(),
        Mock(),
        Mock(),
    )
    kwargs = dict(allow_list=[COMMAND1], deny_list=[COMMAND3], contexts=[CONTEXT1])
    mock_sources_configuration.return_value = {
        SOURCE1: {},
        SOURCE2: {DENY_LIST: [COMMAND2]},
    }
    mock_read_commands.side_effect = [[command1, command2], [command3, command4]]
    commands_map = read_commands_map([], **kwargs)
    assert_sources(commands_map, [SOURCE1, SOURCE2])
    assert_commands(commands_map, SOURCE1, [command1, command2])
    assert_commands(commands_map, SOURCE2, [command3, command4])
    assert_calls(
        mock_read_commands,
        [
            call(**kwargs),
            call(
                allow_list=[COMMAND1],
                deny_list=[COMMAND3, COMMAND2],
                contexts=[CONTEXT1],
            ),
        ],
    )
