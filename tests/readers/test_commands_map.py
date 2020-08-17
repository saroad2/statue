from statue.command import Command
from statue.commands_map import get_commands_map
from statue.constants import COMMANDS
from tests.conftest import (
    ARG1,
    ARG2,
    ARG3,
    ARG4,
    ARG5,
    COMMAND1,
    COMMAND2,
    COMMAND3,
    COMMAND4,
    CONTEXT2,
    HELP_STRING1,
    HELP_STRING2,
    HELP_STRING4,
    HELP_STRING3,
    SOURCE1,
    SOURCE2,
    SOURCE3,
    SOURCE4,
    SOURCE5,
)


def add_commands_section(statue_config, commands_config):
    statue_config[COMMANDS] = commands_config
    return statue_config


def assert_sources(commands_map, sources):
    assert (
        list(commands_map.keys()) == sources
    ), "Commands map doesn't include all sources"


def assert_commands(commands_map, source, commands):
    assert (
        commands_map[source] == commands
    ), f"Commands of {source} are different than expected"


def test_get_commands_map_on_none_empty_source_list(one_command_with_args_settings):
    commands_map = get_commands_map(
        [SOURCE1], add_commands_section({}, one_command_with_args_settings)
    )
    assert_sources(commands_map, [SOURCE1])
    assert_commands(
        commands_map,
        SOURCE1,
        [Command(name=COMMAND1, help=HELP_STRING1, args=[ARG1, ARG2])],
    )


def test_get_commands_map_with_no_sources_list_and_in_input_and_config(
    one_command_with_args_settings,
):
    commands_map = get_commands_map(
        [], add_commands_section({}, one_command_with_args_settings)
    )
    assert commands_map is None


def test_get_commands_map_with_no_sources_and_empty_settings(
    one_command_with_args_settings, empty_settings
):
    commands_map = get_commands_map(
        [], add_commands_section(empty_settings, one_command_with_args_settings)
    )
    assert commands_map is None


def test_get_commands_map_with_existing_config_file(
    non_empty_sources_config, full_commands_settings_with_boolean_contexts
):
    commands_map = get_commands_map(
        [],
        add_commands_section(
            non_empty_sources_config, full_commands_settings_with_boolean_contexts
        ),
    )
    assert_sources(commands_map, [SOURCE1, SOURCE2, SOURCE3, SOURCE4, SOURCE5])
    assert_commands(
        commands_map,
        SOURCE1,
        [
            Command(name=COMMAND1, help=HELP_STRING1, args=[ARG1, ARG2]),
            Command(name=COMMAND2, help=HELP_STRING2, args=[ARG3]),
            Command(name=COMMAND3, help=HELP_STRING3, args=[]),
            Command(name=COMMAND4, help=HELP_STRING4, args=[ARG4, ARG5]),
        ],
    )
    assert_commands(
        commands_map,
        SOURCE2,
        [Command(name=COMMAND1, help=HELP_STRING1, args=[ARG1, ARG2])],
    )
    assert_commands(
        commands_map,
        SOURCE3,
        [
            Command(name=COMMAND1, help=HELP_STRING1, args=[ARG1, ARG2]),
            Command(name=COMMAND2, help=HELP_STRING2, args=[ARG3]),
        ],
    )
    assert_commands(
        commands_map,
        SOURCE4,
        [
            Command(name=COMMAND1, help=HELP_STRING1, args=[ARG1, ARG2]),
            Command(name=COMMAND3, help=HELP_STRING3, args=[]),
            Command(name=COMMAND4, help=HELP_STRING4, args=[ARG4, ARG5],),
        ],
    )
    assert_commands(
        commands_map,
        SOURCE5,
        [
            Command(name=COMMAND1, help=HELP_STRING1, args=[ARG1, ARG2]),
            Command(name=COMMAND2, help=HELP_STRING2, args=[ARG3]),
            Command(name=COMMAND3, help=HELP_STRING3, args=[]),
            Command(name=COMMAND4, help=HELP_STRING4, args=[ARG4, ARG5],),
        ],
    )


def test_get_commands_map_with_global_context(
    non_empty_sources_config, full_commands_settings_with_boolean_contexts
):
    commands_map = get_commands_map(
        [],
        add_commands_section(
            non_empty_sources_config, full_commands_settings_with_boolean_contexts
        ),
        contexts=[CONTEXT2],
    )
    assert_sources(commands_map, [SOURCE1, SOURCE2, SOURCE3, SOURCE4, SOURCE5])
    assert_commands(
        commands_map,
        SOURCE1,
        [
            Command(name=COMMAND1, help=HELP_STRING1, args=[ARG1, ARG2]),
            Command(name=COMMAND2, help=HELP_STRING2, args=[ARG3]),
        ],
    )
    assert_commands(
        commands_map,
        SOURCE2,
        [Command(name=COMMAND1, help=HELP_STRING1, args=[ARG1, ARG2])],
    )
    assert_commands(
        commands_map,
        SOURCE3,
        [
            Command(name=COMMAND1, help=HELP_STRING1, args=[ARG1, ARG2]),
            Command(name=COMMAND2, help=HELP_STRING2, args=[ARG3]),
        ],
    )
    assert_commands(
        commands_map,
        SOURCE4,
        [Command(name=COMMAND1, help=HELP_STRING1, args=[ARG1, ARG2])],
    )
    assert_commands(
        commands_map,
        SOURCE5,
        [
            Command(name=COMMAND1, help=HELP_STRING1, args=[ARG1, ARG2]),
            Command(name=COMMAND2, help=HELP_STRING2, args=[ARG3]),
        ],
    )


def test_get_commands_map_with_global_allow_list(
    non_empty_sources_config, full_commands_settings_with_boolean_contexts
):
    commands_map = get_commands_map(
        [],
        add_commands_section(
            non_empty_sources_config, full_commands_settings_with_boolean_contexts
        ),
        allow_list=[COMMAND1, COMMAND3],
    )
    assert_sources(commands_map, [SOURCE1, SOURCE2, SOURCE3, SOURCE4, SOURCE5])
    assert_commands(
        commands_map,
        SOURCE1,
        [
            Command(name=COMMAND1, help=HELP_STRING1, args=[ARG1, ARG2]),
            Command(name=COMMAND3, help=HELP_STRING3, args=[]),
        ],
    )
    assert_commands(
        commands_map,
        SOURCE2,
        [Command(name=COMMAND1, help=HELP_STRING1, args=[ARG1, ARG2])],
    )
    assert_commands(
        commands_map,
        SOURCE3,
        [Command(name=COMMAND1, help=HELP_STRING1, args=[ARG1, ARG2])],
    )
    assert_commands(
        commands_map,
        SOURCE5,
        [
            Command(name=COMMAND1, help=HELP_STRING1, args=[ARG1, ARG2]),
            Command(name=COMMAND3, help=HELP_STRING3, args=[]),
        ],
    )


def test_get_commands_map_with_global_deny_list(
    non_empty_sources_config, full_commands_settings_with_boolean_contexts
):
    commands_map = get_commands_map(
        [],
        add_commands_section(
            non_empty_sources_config, full_commands_settings_with_boolean_contexts
        ),
        deny_list=[COMMAND4],
    )
    assert_sources(commands_map, [SOURCE1, SOURCE2, SOURCE3, SOURCE4, SOURCE5])
    assert_commands(
        commands_map,
        SOURCE1,
        [
            Command(name=COMMAND1, help=HELP_STRING1, args=[ARG1, ARG2]),
            Command(name=COMMAND2, help=HELP_STRING2, args=[ARG3]),
            Command(name=COMMAND3, help=HELP_STRING3, args=[]),
        ],
    )
    assert_commands(
        commands_map,
        SOURCE2,
        [Command(name=COMMAND1, help=HELP_STRING1, args=[ARG1, ARG2])],
    )
    assert_commands(
        commands_map,
        SOURCE3,
        [
            Command(name=COMMAND1, help=HELP_STRING1, args=[ARG1, ARG2]),
            Command(name=COMMAND2, help=HELP_STRING2, args=[ARG3]),
        ],
    )
    assert_commands(
        commands_map,
        SOURCE5,
        [
            Command(name=COMMAND1, help=HELP_STRING1, args=[ARG1, ARG2]),
            Command(name=COMMAND2, help=HELP_STRING2, args=[ARG3]),
            Command(name=COMMAND3, help=HELP_STRING3, args=[]),
        ],
    )
