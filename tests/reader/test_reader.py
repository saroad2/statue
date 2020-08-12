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
    CONTEXT1,
    CONTEXT2,
    CONTEXT3,
    CONTEXT4,
    NOT_EXISTING_CONTEXT,
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


def test_read_settings_with_multiple_commands(full_settings_with_boolean_contexts):
    commands = read_commands(SETTINGS_FILE_PATH)
    assert commands == [
        Command(name=COMMAND1, help=HELP_STRING1, args=[ARG1, ARG2]),
        Command(name=COMMAND2, help=HELP_STRING2, args=[ARG3]),
        Command(name=COMMAND3, help=HELP_STRING3),
        Command(name=COMMAND4, help=HELP_STRING4, args=[ARG4, ARG5]),
    ]


def test_read_settings_with_non_passing_context(full_settings_with_boolean_contexts):
    commands = read_commands(SETTINGS_FILE_PATH, contexts=[NOT_EXISTING_CONTEXT])
    assert commands == []


def test_read_settings_with_one_passing_context(full_settings_with_boolean_contexts):
    commands = read_commands(SETTINGS_FILE_PATH, contexts=[CONTEXT3])
    assert commands == [Command(name=COMMAND3, help=HELP_STRING3)]


def test_read_settings_with_two_passing_context(full_settings_with_boolean_contexts):
    commands = read_commands(SETTINGS_FILE_PATH, contexts=[CONTEXT2])
    assert commands == [
        Command(name=COMMAND1, help=HELP_STRING1, args=[ARG1, ARG2]),
        Command(name=COMMAND2, help=HELP_STRING2, args=[ARG3]),
    ]


def test_read_settings_with_two_contexts(full_settings_with_boolean_contexts):
    commands = read_commands(SETTINGS_FILE_PATH, contexts=[CONTEXT1, CONTEXT2])
    assert commands == [
        Command(name=COMMAND1, help=HELP_STRING1, args=[ARG1, ARG2]),
    ]


def test_read_settings_with_non_standard_command(full_settings_with_boolean_contexts):
    commands = read_commands(SETTINGS_FILE_PATH, contexts=[CONTEXT4])
    assert commands == [
        Command(name=COMMAND5, help=HELP_STRING5),
    ]


def test_read_settings_with_overrides_without_contexts(
    full_settings_with_override_contexts,
):
    commands = read_commands(SETTINGS_FILE_PATH)
    assert commands == [
        Command(name=COMMAND1, help=HELP_STRING1, args=[ARG1, ARG2]),
    ]


def test_read_settings_with_overrides_with_context(full_settings_with_override_contexts,):
    commands = read_commands(SETTINGS_FILE_PATH, contexts=[CONTEXT1])
    assert commands == [
        Command(name=COMMAND1, help=HELP_STRING1, args=[ARG3]),
    ]


def test_read_settings_with_overrides_with_another_context(
    full_settings_with_override_contexts,
):
    commands = read_commands(SETTINGS_FILE_PATH, contexts=[CONTEXT2])
    assert commands == [
        Command(name=COMMAND1, help=HELP_STRING1, args=[ARG4, ARG5]),
    ]


def test_read_settings_with_overrides_with_clear_args_context(
    full_settings_with_override_contexts,
):
    commands = read_commands(SETTINGS_FILE_PATH, contexts=[CONTEXT3])
    assert commands == [
        Command(name=COMMAND1, help=HELP_STRING1, args=[]),
    ]


def test_read_settings_with_overrides_with_add_args_context(
    full_settings_with_override_contexts,
):
    commands = read_commands(SETTINGS_FILE_PATH, contexts=[CONTEXT4])
    assert commands == [
        Command(name=COMMAND1, help=HELP_STRING1, args=[ARG1, ARG2, ARG5]),
    ]


def test_read_commands_with_allow_list(full_settings_with_boolean_contexts):
    commands = read_commands(SETTINGS_FILE_PATH, allow_list=[COMMAND1, COMMAND3])
    assert commands == [
        Command(name=COMMAND1, help=HELP_STRING1, args=[ARG1, ARG2],),
        Command(name=COMMAND3, help=HELP_STRING3, args=[]),
    ]


def test_read_commands_with_deny_list(full_settings_with_boolean_contexts):
    commands = read_commands(SETTINGS_FILE_PATH, deny_list=[COMMAND1, COMMAND3])
    assert commands == [
        Command(name=COMMAND2, help=HELP_STRING2, args=[ARG3],),
        Command(name=COMMAND4, help=HELP_STRING4, args=[ARG4, ARG5]),
    ]
