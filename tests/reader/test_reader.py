from statue.command import Command
from statue.reader import read_commands
from tests.reader.conftest import (
    SETTINGS_FILE_PATH,
    COMMAND1,
    COMMAND2,
    COMMAND3,
    COMMAND4,
    COMMAND5,
    HELP_STRING1,
    HELP_STRING2,
    HELP_STRING3,
    HELP_STRING4,
    HELP_STRING5,
    ARG1,
    ARG2,
    ARG3,
    ARG4,
    ARG5,
    FILTER1,
    FILTER2,
    FILTER3,
    FILTER4,
    NOT_EXISTING_FILTER,
)


def test_read_empty_settings(empty_settings):
    commands = read_commands(SETTINGS_FILE_PATH)
    assert commands == []


def test_read_settings_with_one_command_without_args(one_command_setting):
    commands = read_commands(SETTINGS_FILE_PATH)
    assert commands == [Command(name=COMMAND1, help=HELP_STRING1)]


def test_read_settings_with_one_command_with_args(one_command_with_args_settings):
    commands = read_commands(SETTINGS_FILE_PATH)
    assert commands == [Command(name=COMMAND1, help=HELP_STRING1, args=[ARG1, ARG2])]


def test_read_settings_with_multiple_commands(full_settings_with_boolean_filters):
    commands = read_commands(SETTINGS_FILE_PATH)
    assert commands == [
        Command(name=COMMAND1, help=HELP_STRING1, args=[ARG1, ARG2]),
        Command(name=COMMAND2, help=HELP_STRING2, args=[ARG3]),
        Command(name=COMMAND3, help=HELP_STRING3),
        Command(name=COMMAND4, help=HELP_STRING4, args=[ARG4, ARG5]),
    ]


def test_read_settings_with_non_passing_filter(full_settings_with_boolean_filters):
    commands = read_commands(SETTINGS_FILE_PATH, filters=[NOT_EXISTING_FILTER])
    assert commands == []


def test_read_settings_with_one_passing_filter(full_settings_with_boolean_filters):
    commands = read_commands(SETTINGS_FILE_PATH, filters=[FILTER3])
    assert commands == [Command(name=COMMAND3, help=HELP_STRING3)]


def test_read_settings_with_two_passing_filter(full_settings_with_boolean_filters):
    commands = read_commands(SETTINGS_FILE_PATH, filters=[FILTER2])
    assert commands == [
        Command(name=COMMAND1, help=HELP_STRING1, args=[ARG1, ARG2]),
        Command(name=COMMAND2, help=HELP_STRING2, args=[ARG3]),
    ]


def test_read_settings_with_two_filters(full_settings_with_boolean_filters):
    commands = read_commands(SETTINGS_FILE_PATH, filters=[FILTER1, FILTER2])
    assert commands == [
        Command(name=COMMAND1, help=HELP_STRING1, args=[ARG1, ARG2]),
    ]


def test_read_settings_with_non_standard_command(full_settings_with_boolean_filters):
    commands = read_commands(SETTINGS_FILE_PATH, filters=[FILTER4])
    assert commands == [
        Command(name=COMMAND5, help=HELP_STRING5),
    ]


def test_read_settings_with_overrides_without_filters(
    full_settings_with_override_filters,
):
    commands = read_commands(SETTINGS_FILE_PATH)
    assert commands == [
        Command(name=COMMAND1, help=HELP_STRING1, args=[ARG1, ARG2]),
    ]


def test_read_settings_with_overrides_with_filter(full_settings_with_override_filters,):
    commands = read_commands(SETTINGS_FILE_PATH, filters=[FILTER1])
    assert commands == [
        Command(name=COMMAND1, help=HELP_STRING1, args=[ARG3]),
    ]


def test_read_settings_with_overrides_with_another_filter(
    full_settings_with_override_filters,
):
    commands = read_commands(SETTINGS_FILE_PATH, filters=[FILTER2])
    assert commands == [
        Command(name=COMMAND1, help=HELP_STRING1, args=[ARG4, ARG5]),
    ]


def test_read_settings_with_overrides_with_clear_args_filter(
    full_settings_with_override_filters,
):
    commands = read_commands(SETTINGS_FILE_PATH, filters=[FILTER3])
    assert commands == [
        Command(name=COMMAND1, help=HELP_STRING1, args=[]),
    ]
