from collections import OrderedDict

import pytest

from statue.config.commands_repository import CommandsRepository
from statue.exceptions import UnknownCommand
from tests.constants import ARG1, ARG2, COMMAND1, COMMAND2, COMMAND3, COMMAND4, COMMAND5
from tests.util import command_builder_mock


def test_commands_repository_empty_constructor():
    commands_repository = CommandsRepository()

    assert len(commands_repository) == 0
    assert not commands_repository.command_names_list
    assert not list(commands_repository)

    assert not commands_repository.has_command(COMMAND1)


def test_commands_repository_construct_with_one_command_builder():
    command_builder = command_builder_mock(name=COMMAND1)
    commands_repository = CommandsRepository(command_builder)

    assert len(commands_repository) == 1
    assert commands_repository.command_names_list == [COMMAND1]
    assert list(commands_repository) == [command_builder]
    assert commands_repository[COMMAND1] == command_builder
    assert commands_repository.has_command(COMMAND1)
    assert not commands_repository.has_command(COMMAND2)


def test_commands_repository_construct_with_two_command_builders():
    command_builder1, command_builder2 = (
        command_builder_mock(name=COMMAND1),
        command_builder_mock(name=COMMAND2),
    )
    commands_repository = CommandsRepository(command_builder1, command_builder2)

    assert len(commands_repository) == 2
    assert commands_repository.command_names_list == [COMMAND1, COMMAND2]
    assert list(commands_repository) == [
        command_builder1,
        command_builder2,
    ]
    assert commands_repository[COMMAND1] == command_builder1
    assert commands_repository[COMMAND2] == command_builder2
    assert commands_repository.has_command(COMMAND1)
    assert commands_repository.has_command(COMMAND2)
    assert not commands_repository.has_command(COMMAND3)


def test_commands_repository_construct_add_one_command_builder():
    command_builder1, command_builder2, command_builder3 = (
        command_builder_mock(name=COMMAND1),
        command_builder_mock(name=COMMAND2),
        command_builder_mock(name=COMMAND3),
    )
    commands_repository = CommandsRepository(command_builder1, command_builder2)
    commands_repository.add_command_builders(command_builder3)

    assert len(commands_repository) == 3
    assert commands_repository.command_names_list == [COMMAND1, COMMAND2, COMMAND3]
    assert list(commands_repository) == [
        command_builder1,
        command_builder2,
        command_builder3,
    ]
    assert commands_repository[COMMAND1] == command_builder1
    assert commands_repository[COMMAND2] == command_builder2
    assert commands_repository[COMMAND3] == command_builder3
    assert commands_repository.has_command(COMMAND1)
    assert commands_repository.has_command(COMMAND2)
    assert commands_repository.has_command(COMMAND3)
    assert not commands_repository.has_command(COMMAND4)


def test_commands_repository_construct_add_two_command_builders():
    command_builder1, command_builder2, command_builder3, command_builder4 = (
        command_builder_mock(name=COMMAND1),
        command_builder_mock(name=COMMAND2),
        command_builder_mock(name=COMMAND3),
        command_builder_mock(name=COMMAND4),
    )
    commands_repository = CommandsRepository(command_builder1, command_builder2)
    commands_repository.add_command_builders(command_builder3, command_builder4)

    assert len(commands_repository) == 4
    assert commands_repository.command_names_list == [
        COMMAND1,
        COMMAND2,
        COMMAND3,
        COMMAND4,
    ]
    assert list(commands_repository) == [
        command_builder1,
        command_builder2,
        command_builder3,
        command_builder4,
    ]
    assert commands_repository[COMMAND1] == command_builder1
    assert commands_repository[COMMAND2] == command_builder2
    assert commands_repository[COMMAND3] == command_builder3
    assert commands_repository[COMMAND4] == command_builder4
    assert commands_repository.has_command(COMMAND1)
    assert commands_repository.has_command(COMMAND2)
    assert commands_repository.has_command(COMMAND3)
    assert commands_repository.has_command(COMMAND4)
    assert not commands_repository.has_command(COMMAND5)


def test_commands_repository_add_command_overrides_existing():
    command_builder1, command_builder2 = (
        command_builder_mock(name=COMMAND1),
        command_builder_mock(name=COMMAND1, default_args=[ARG1, ARG2]),
    )
    commands_repository = CommandsRepository()

    commands_repository.add_command_builders(command_builder1)
    assert commands_repository[COMMAND1] == command_builder1

    commands_repository.add_command_builders(command_builder2)
    assert commands_repository[COMMAND1] != command_builder1
    assert commands_repository[COMMAND1] == command_builder2
    assert commands_repository.has_command(COMMAND1)
    assert not commands_repository.has_command(COMMAND2)


def test_commands_repository_reset():
    command_builder1, command_builder2 = (
        command_builder_mock(name=COMMAND1),
        command_builder_mock(name=COMMAND2),
    )
    commands_repository = CommandsRepository()
    commands_repository.add_command_builders(command_builder1, command_builder2)

    commands_repository.reset()

    assert len(commands_repository) == 0
    assert not commands_repository.command_names_list
    assert not list(commands_repository)
    assert not commands_repository.has_command(COMMAND1)
    assert not commands_repository.has_command(COMMAND2)


def test_commands_repository_as_dict():
    command_builder1, command_builder2, command_builder3 = (
        command_builder_mock(name=COMMAND1),
        command_builder_mock(name=COMMAND2),
        command_builder_mock(name=COMMAND3),
    )

    commands_repository = CommandsRepository(
        command_builder1, command_builder3, command_builder2
    )
    commands_repository_dict = commands_repository.as_dict()

    assert isinstance(commands_repository_dict, OrderedDict)
    assert list(commands_repository_dict.keys()) == [COMMAND1, COMMAND2, COMMAND3]
    assert commands_repository_dict[COMMAND1] == command_builder1.as_dict.return_value
    assert commands_repository_dict[COMMAND2] == command_builder2.as_dict.return_value
    assert commands_repository_dict[COMMAND3] == command_builder3.as_dict.return_value


def test_commands_repository_get_non_existing_command():
    command_builder1, command_builder2 = (
        command_builder_mock(name=COMMAND1),
        command_builder_mock(name=COMMAND2),
    )
    commands_repository = CommandsRepository()
    commands_repository.add_command_builders(command_builder1, command_builder2)

    with pytest.raises(
        UnknownCommand, match=f'^Could not find command named "{COMMAND3}"$'
    ):
        commands_repository[COMMAND3]  # pylint: disable=W0104
