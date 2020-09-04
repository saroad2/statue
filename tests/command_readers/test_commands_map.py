from unittest import mock

from statue.commands_map import get_commands_map
from statue.constants import ALLOW_LIST, CONTEXTS, DENY_LIST
from tests.constants import (
    ARG1,
    ARG2,
    ARG3,
    ARG4,
    ARG5,
    COMMAND1,
    COMMAND2,
    COMMAND3,
    COMMAND4,
    COMMAND_HELP_STRING1,
    COMMAND_HELP_STRING2,
    COMMAND_HELP_STRING3,
    COMMAND_HELP_STRING4,
    CONTEXT1,
    CONTEXT2,
    SOURCE1,
    SOURCE2,
    SOURCE3,
    SOURCE4,
    SOURCE5,
)


def assert_sources(commands_map, sources):
    assert (
        list(commands_map.keys()) == sources
    ), "Commands map doesn't include all sources"


def assert_commands(commands_map, source, commands):
    assert (
        commands_map[source] == commands
    ), f"Commands of {source} are different than expected"


def assert_read_commands(read_commands, *calls):
    assert read_commands.call_count == len(
        calls
    ), "read_commands number of calls is different than expected"
    for i, call_kwargs in enumerate(calls):
        assert read_commands.call_args_list[i] == mock.call(
            **call_kwargs
        ), f"read_commands call number {i} is different than expected."


def test_get_commands_map_on_none_empty_source_list(mock_read_commands):
    command = mock.Mock()
    mock_read_commands.return_value = [command]
    commands_map = get_commands_map([SOURCE1])
    assert_sources(commands_map, [SOURCE1])
    assert_commands(commands_map, SOURCE1, [command])


def test_get_commands_map_with_no_sources(
    mock_sources_configuration, mock_read_commands
):
    mock_sources_configuration.return_value = None
    commands_map = get_commands_map([])
    assert commands_map is None
    mock_read_commands.assert_not_called()


def test_get_commands_map_with_no_commands(
    mock_sources_configuration, mock_read_commands
):
    kwargs = dict(allow_list=[COMMAND1], deny_list=[COMMAND3], contexts=[CONTEXT2])
    mock_sources_configuration.return_value = {SOURCE1: {}, SOURCE2: {}}
    mock_read_commands.return_value = None
    commands_map = get_commands_map([], **kwargs)
    assert commands_map is None
    assert_read_commands(mock_read_commands, kwargs, kwargs)


def test_get_commands_map_with_commands_without_directives(
    mock_sources_configuration, mock_read_commands
):
    command1, command2, command3 = mock.Mock(), mock.Mock(), mock.Mock()
    mock_sources_configuration.return_value = {SOURCE1: {}, SOURCE2: {}}
    mock_read_commands.side_effect = [[command1], [command2, command3]]
    commands_map = get_commands_map([])
    assert_sources(commands_map, [SOURCE1, SOURCE2])
    assert_commands(commands_map, SOURCE1, [command1])
    assert_commands(commands_map, SOURCE2, [command2, command3])
    empty_kwargs = dict(allow_list=None, contexts=None, deny_list=None)
    assert_read_commands(mock_read_commands, empty_kwargs, empty_kwargs)


def test_get_commands_map_with_commands_and_directives(
    mock_sources_configuration, mock_read_commands
):
    command1, command2, command3 = mock.Mock(), mock.Mock(), mock.Mock()
    kwargs = dict(allow_list=[COMMAND1], deny_list=[COMMAND3], contexts=[CONTEXT2])
    mock_sources_configuration.return_value = {SOURCE1: {}, SOURCE2: {}}
    mock_read_commands.side_effect = [[command1], [command2, command3]]
    commands_map = get_commands_map([], **kwargs)
    assert_sources(commands_map, [SOURCE1, SOURCE2])
    assert_commands(commands_map, SOURCE1, [command1])
    assert_commands(commands_map, SOURCE2, [command2, command3])
    assert_read_commands(mock_read_commands, kwargs, kwargs)


def test_get_commands_map_with_source_context(
    mock_sources_configuration, mock_read_commands
):
    command1, command2, command3 = mock.Mock(), mock.Mock(), mock.Mock()
    kwargs = dict(allow_list=[COMMAND1], deny_list=[COMMAND3], contexts=[CONTEXT2])
    mock_sources_configuration.return_value = {
        SOURCE1: {CONTEXTS: [CONTEXT1]},
        SOURCE2: {},
    }
    mock_read_commands.side_effect = [[command1, command2], [command3]]
    commands_map = get_commands_map([], **kwargs)
    assert_sources(commands_map, [SOURCE1, SOURCE2])
    assert_commands(commands_map, SOURCE1, [command1, command2])
    assert_commands(commands_map, SOURCE2, [command3])
    assert_read_commands(
        mock_read_commands,
        dict(
            allow_list=[COMMAND1], deny_list=[COMMAND3], contexts=[CONTEXT2, CONTEXT1]
        ),
        kwargs,
    )


def test_get_commands_map_with_source_allow_list(
    mock_sources_configuration, mock_read_commands
):
    command1, command2 = mock.Mock(), mock.Mock()
    kwargs = dict(
        allow_list=[COMMAND1, COMMAND2], deny_list=[COMMAND3], contexts=[CONTEXT1]
    )
    mock_sources_configuration.return_value = {
        SOURCE1: {},
        SOURCE2: {ALLOW_LIST: [COMMAND2]},
    }
    mock_read_commands.side_effect = [[command1], [command2]]
    commands_map = get_commands_map([], **kwargs)
    assert_sources(commands_map, [SOURCE1, SOURCE2])
    assert_commands(commands_map, SOURCE1, [command1])
    assert_commands(commands_map, SOURCE2, [command2])
    assert_read_commands(
        mock_read_commands,
        kwargs,
        dict(allow_list=[COMMAND2], deny_list=[COMMAND3], contexts=[CONTEXT1]),
    )


def test_get_commands_map_with_source_deny_list(
    mock_sources_configuration, mock_read_commands
):
    command1, command2, command3, command4 = (
        mock.Mock(),
        mock.Mock(),
        mock.Mock(),
        mock.Mock(),
    )
    kwargs = dict(allow_list=[COMMAND1], deny_list=[COMMAND3], contexts=[CONTEXT1])
    mock_sources_configuration.return_value = {
        SOURCE1: {},
        SOURCE2: {DENY_LIST: [COMMAND2]},
    }
    mock_read_commands.side_effect = [[command1, command2], [command3, command4]]
    commands_map = get_commands_map([], **kwargs)
    assert_sources(commands_map, [SOURCE1, SOURCE2])
    assert_commands(commands_map, SOURCE1, [command1, command2])
    assert_commands(commands_map, SOURCE2, [command3, command4])
    assert_read_commands(
        mock_read_commands,
        kwargs,
        dict(
            allow_list=[COMMAND1], deny_list=[COMMAND3, COMMAND2], contexts=[CONTEXT1]
        ),
    )
