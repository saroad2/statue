import pytest

from statue.command import Command
from statue.configuration import Configuration
from statue.constants import COMMANDS, CONTEXTS
from statue.excptions import (
    InvalidCommand,
    MissingConfiguration,
    UnknownCommand,
    UnknownContext,
)
from tests.constants import (
    ARG1,
    ARG2,
    ARG3,
    ARG4,
    ARG5,
    COMMAND1,
    COMMAND2,
    COMMAND3,
    COMMAND5,
    COMMAND_HELP_STRING1,
    COMMAND_HELP_STRING2,
    COMMAND_HELP_STRING3,
    COMMAND_HELP_STRING5,
    CONTEXT1,
    CONTEXT2,
    CONTEXT3,
    CONTEXT4,
    NOT_EXISTING_CONTEXT,
    OVERRIDE_COMMANDS_CONFIGURATION,
)


def test_read_command_with_no_contexts(
    full_commands_settings_with_boolean_contexts,
):
    command = Configuration.read_command(command_name=COMMAND1)
    assert command == Command(
        name=COMMAND1, help=COMMAND_HELP_STRING1, args=[ARG1, ARG2]
    ), "Command is different than exp expected"


def test_read_command_with_non_passing_context(
    full_commands_settings_with_boolean_contexts,
):
    with pytest.raises(
        UnknownContext,
        match=f'^Could not find context named "{NOT_EXISTING_CONTEXT}".$',
    ):
        Configuration.read_command(
            command_name=COMMAND1, contexts=[NOT_EXISTING_CONTEXT]
        )


def test_read_command_with_passing_context(
    full_commands_settings_with_boolean_contexts,
):
    command = Configuration.read_command(command_name=COMMAND1, contexts=[CONTEXT2])
    assert command == Command(
        name=COMMAND1, help=COMMAND_HELP_STRING1, args=[ARG1, ARG2]
    ), "Command is different than expected."


def test_read_command_with_two_contexts(full_commands_settings_with_boolean_contexts):
    command = Configuration.read_command(
        command_name=COMMAND1, contexts=[CONTEXT1, CONTEXT2]
    )
    assert command == Command(
        name=COMMAND1, help=COMMAND_HELP_STRING1, args=[ARG1, ARG2]
    ), "Command is different than expected."


def test_read_command_with_non_standard_command(
    full_commands_settings_with_boolean_contexts,
):
    command = Configuration.read_command(command_name=COMMAND5, contexts=[CONTEXT4])
    assert command == Command(
        name=COMMAND5, help=COMMAND_HELP_STRING5
    ), "Command is different than expected."


def test_read_command_with_overrides_without_contexts(
    full_commands_settings,
):
    command = Configuration.read_command(command_name=COMMAND1)
    assert command == Command(
        name=COMMAND1, help=COMMAND_HELP_STRING1, args=[ARG1, ARG2]
    ), "Command is different than expected."


def test_read_command_with_overrides_with_context(
    full_commands_settings,
):
    command = Configuration.read_command(command_name=COMMAND1, contexts=[CONTEXT1])
    assert command == Command(
        name=COMMAND1, help=COMMAND_HELP_STRING1, args=[ARG3]
    ), "Command is different than expected."


def test_read_command_with_overrides_with_another_context(
    full_commands_settings,
):
    command = Configuration.read_command(command_name=COMMAND1, contexts=[CONTEXT2])
    assert command == Command(
        name=COMMAND1, help=COMMAND_HELP_STRING1, args=[ARG4, ARG5]
    ), "Command is different than expected."


def test_read_command_with_overrides_with_clear_args_context(
    full_commands_settings,
):
    command = Configuration.read_command(command_name=COMMAND1, contexts=[CONTEXT3])
    assert command == Command(
        name=COMMAND1, help=COMMAND_HELP_STRING1, args=[]
    ), "Command is different than expected."


def test_read_command_with_overrides_with_add_args_context(
    full_commands_settings,
):
    command = Configuration.read_command(command_name=COMMAND1, contexts=[CONTEXT4])
    assert command == Command(
        name=COMMAND1, help=COMMAND_HELP_STRING1, args=[ARG1, ARG2, ARG5]
    ), "Command is different than expected."


def test_read_command_twice_with_overrides_with_add_args_context(
    full_commands_settings,
):
    command1 = Configuration.read_command(command_name=COMMAND1, contexts=[CONTEXT4])
    assert command1 == Command(
        name=COMMAND1, help=COMMAND_HELP_STRING1, args=[ARG1, ARG2, ARG5]
    ), "Command is different than expected in first read."
    command2 = Configuration.read_command(
        command_name=COMMAND1,
    )
    assert command2 == Command(
        name=COMMAND1, help=COMMAND_HELP_STRING1, args=[ARG1, ARG2]
    ), "Command is different than expected in second read."


def test_read_command_with_empty_allow_list(
    full_commands_settings_with_boolean_contexts,
):
    command = Configuration.read_command(command_name=COMMAND1, allow_list=[])
    assert command == Command(
        name=COMMAND1, help=COMMAND_HELP_STRING1, args=[ARG1, ARG2]
    ), "Command is different than expected."


def test_read_command_in_allow_list(
    full_commands_settings_with_boolean_contexts,
):
    command = Configuration.read_command(
        command_name=COMMAND1, allow_list=[COMMAND1, COMMAND3]
    )
    assert command == Command(
        name=COMMAND1,
        help=COMMAND_HELP_STRING1,
        args=[ARG1, ARG2],
    ), "Command is different than expected."


def test_read_command_not_in_allow_list(
    full_commands_settings_with_boolean_contexts,
):
    with pytest.raises(
        InvalidCommand,
        match=(
            f'The command "{COMMAND1}" does not match the restrictions: '
            fr"contexts=None, allow_list=\['{COMMAND2}', '{COMMAND3}'\], deny_list=None"
        ),
    ):
        Configuration.read_command(
            command_name=COMMAND1, allow_list=[COMMAND2, COMMAND3]
        )


def test_read_command_not_in_deny_list(full_commands_settings_with_boolean_contexts):
    command = Configuration.read_command(
        command_name=COMMAND1, deny_list=[COMMAND2, COMMAND3]
    )
    assert command == Command(
        name=COMMAND1,
        help=COMMAND_HELP_STRING1,
        args=[ARG1, ARG2],
    ), "Command is different than expected."


def test_read_command_in_deny_list(full_commands_settings_with_boolean_contexts):
    with pytest.raises(
        InvalidCommand,
        match=(
            f'The command "{COMMAND1}" does not match the restrictions: '
            fr"contexts=None, allow_list=None, deny_list=\['{COMMAND1}', '{COMMAND3}'\]"
        ),
    ):
        Configuration.read_command(
            command_name=COMMAND1, deny_list=[COMMAND1, COMMAND3]
        )


def test_read_command_non_existing(full_commands_settings):
    with pytest.raises(
        UnknownCommand,
        match=f'^Could not find command named "{COMMAND5}".$',
    ):
        Configuration.read_command(command_name=COMMAND5)


def test_read_command_with_no_commands_configuration(configuration_without_commands):
    with pytest.raises(
        UnknownCommand,
        match=f'^Could not find command named "{COMMAND5}".$',
    ):
        Configuration.read_command(command_name=COMMAND5)


def test_read_command_with_context_when_no_context_configuration_was_set(
    clear_configuration,
):
    Configuration.statue_configuration = {COMMANDS: OVERRIDE_COMMANDS_CONFIGURATION}
    with pytest.raises(
        MissingConfiguration,
        match=f'^"{CONTEXTS}" is missing from Statue configuration.$',
    ):
        Configuration.read_command(command_name=COMMAND1, contexts=[CONTEXT1])


def test_read_command_with_no_context_in_context_inheritance(
    commands_settings_with_context_inheritance,
):
    command = Configuration.read_command(command_name=COMMAND3, contexts=[])
    assert command == Command(
        name=COMMAND3, help=COMMAND_HELP_STRING3, args=[]
    ), "Command is different than expected."


def test_read_command_with_root_context(commands_settings_with_context_inheritance):
    command = Configuration.read_command(command_name=COMMAND3, contexts=[CONTEXT3])
    assert command == Command(
        name=COMMAND3, help=COMMAND_HELP_STRING3, args=[]
    ), "Command is different than expected."


def test_read_command_with_override_context(commands_settings_with_context_inheritance):
    command = Configuration.read_command(command_name=COMMAND2, contexts=[CONTEXT2])
    assert command == Command(
        name=COMMAND2, help=COMMAND_HELP_STRING2, args=[ARG3, ARG5]
    ), "Command is different than expected."


def test_read_command_with_double_inheritance_context(
    commands_settings_with_context_inheritance,
):
    command = Configuration.read_command(command_name=COMMAND3, contexts=[CONTEXT4])
    assert command == Command(
        name=COMMAND3, help=COMMAND_HELP_STRING3, args=[]
    ), "Command is different than expected."
