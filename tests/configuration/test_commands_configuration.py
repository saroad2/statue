import pytest

from statue.command_builder import CommandBuilder
from statue.configuration import Configuration
from statue.constants import COMMANDS
from statue.exceptions import MissingConfiguration, UnknownCommand
from tests.constants import (
    COMMAND1,
    COMMAND2,
    COMMAND3,
    COMMAND4,
    COMMAND_HELP_STRING1,
    COMMAND_HELP_STRING2,
    COMMAND_HELP_STRING3,
)


def test_simple_commands_configuration(clear_configuration):
    command_builders = [
        CommandBuilder(name=COMMAND1, help=COMMAND_HELP_STRING1),
        CommandBuilder(name=COMMAND2, help=COMMAND_HELP_STRING2),
        CommandBuilder(name=COMMAND3, help=COMMAND_HELP_STRING3),
    ]
    commands_configuration = {
        command_builder.name: command_builder for command_builder in command_builders
    }
    Configuration.set_statue_configuration({COMMANDS: commands_configuration})
    assert (
        Configuration.commands_configuration() == commands_configuration
    ), "Commands configuration is different than expected"
    assert Configuration.command_names_list() == [
        COMMAND1,
        COMMAND2,
        COMMAND3,
    ], "Command names list is different than expected"
    assert (
        Configuration.command_builders_list() == command_builders
    ), "Command builders list is different than expected"
    for command_builder in command_builders:
        assert (
            Configuration.get_command_builder(command_builder.name) == command_builder
        ), "Given command builder is different than expected."


def test_empty_commands_configuration(clear_configuration):
    Configuration.set_statue_configuration({})
    assert (
        Configuration.commands_configuration() is None
    ), "Commands configuration is different than expected"
    assert (
        not Configuration.command_names_list()
    ), "Command names list supposed to be empty"
    assert (
        not Configuration.command_builders_list()
    ), "Command builders list supposed to be empty"

    with pytest.raises(
        MissingConfiguration,
        match=f'^"{COMMANDS}" is missing from Statue configuration.$',
    ):
        Configuration.get_command_builder(COMMAND1)


def test_get_unknown_command_builder():
    command_builders = [
        CommandBuilder(name=COMMAND1, help=COMMAND_HELP_STRING1),
        CommandBuilder(name=COMMAND2, help=COMMAND_HELP_STRING2),
        CommandBuilder(name=COMMAND3, help=COMMAND_HELP_STRING3),
    ]
    commands_configuration = {
        command_builder.name: command_builder for command_builder in command_builders
    }
    Configuration.set_statue_configuration({COMMANDS: commands_configuration})

    with pytest.raises(
        UnknownCommand, match=f'^Could not find command named "{COMMAND4}"$'
    ):
        Configuration.get_command_builder(COMMAND4)
