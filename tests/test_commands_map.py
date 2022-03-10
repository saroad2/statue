from statue.commands_map import CommandsMap
from tests.constants import COMMAND1, COMMAND2, COMMAND3, COMMAND4, SOURCE1, SOURCE2
from tests.util import command_mock


def test_empty_commands_map():
    commands_map = CommandsMap()

    assert len(commands_map) == 0
    assert commands_map.total_commands_count == 0
    assert not commands_map.command_names


def test_commands_map_with_one_source_and_one_command():
    commands_map = CommandsMap()
    commands_map[SOURCE1] = [command_mock(name=COMMAND1)]

    assert len(commands_map) == 1
    assert commands_map.total_commands_count == 1
    assert commands_map.command_names == {COMMAND1}


def test_commands_map_with_one_source_and_multiple_commands():
    commands_map = CommandsMap()
    commands_map[SOURCE1] = [
        command_mock(name=COMMAND1),
        command_mock(name=COMMAND2),
        command_mock(name=COMMAND3),
    ]

    assert len(commands_map) == 1
    assert commands_map.total_commands_count == 3
    assert commands_map.command_names == {COMMAND1, COMMAND2, COMMAND3}


def test_commands_map_with_two_sources_one_command_each():
    commands_map = CommandsMap()
    commands_map[SOURCE1] = [command_mock(name=COMMAND1)]
    commands_map[SOURCE2] = [command_mock(name=COMMAND2)]

    assert len(commands_map) == 2
    assert commands_map.total_commands_count == 2
    assert commands_map.command_names == {COMMAND1, COMMAND2}


def test_commands_map_with_two_sources_same_command_each():
    commands_map = CommandsMap()
    commands_map[SOURCE1] = [command_mock(name=COMMAND1)]
    commands_map[SOURCE2] = [command_mock(name=COMMAND1)]

    assert len(commands_map) == 2
    assert commands_map.total_commands_count == 2
    assert commands_map.command_names == {COMMAND1}


def test_commands_map_with_two_sources_multiple_commands():
    commands_map = CommandsMap()
    commands_map[SOURCE1] = [command_mock(name=COMMAND1), command_mock(name=COMMAND2)]
    commands_map[SOURCE2] = [
        command_mock(name=COMMAND3),
        command_mock(name=COMMAND1),
        command_mock(name=COMMAND4),
    ]

    assert len(commands_map) == 2
    assert commands_map.total_commands_count == 5
    assert commands_map.command_names == {COMMAND1, COMMAND2, COMMAND3, COMMAND4}
