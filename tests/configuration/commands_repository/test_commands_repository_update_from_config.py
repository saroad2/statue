import mock

from statue.command_builder import CommandBuilder
from statue.config.commands_repository import CommandsRepository
from tests.constants import COMMAND1, COMMAND2, COMMAND3
from tests.util import command_builder_mock


def test_commands_repository_update_from_empty_config():
    command_builder1, command_builder2, command_builder3 = (
        command_builder_mock(name=COMMAND1),
        command_builder_mock(name=COMMAND2),
        command_builder_mock(name=COMMAND3),
    )
    commands_repository = CommandsRepository()
    commands_repository.add_command_builders(
        command_builder1, command_builder2, command_builder3
    )

    commands_repository.update_from_config({})

    assert len(commands_repository) == 3
    assert commands_repository[COMMAND1] == command_builder1
    assert commands_repository[COMMAND2] == command_builder2
    assert commands_repository[COMMAND3] == command_builder3


def test_commands_repository_update_adds_new_builder():
    command_builder1, command_builder2, command_builder3 = (
        command_builder_mock(name=COMMAND1),
        command_builder_mock(name=COMMAND2),
        command_builder_mock(name=COMMAND3),
    )
    builder_config = mock.Mock()
    commands_repository = CommandsRepository()
    commands_repository.add_command_builders(command_builder1, command_builder2)

    with mock.patch.object(CommandBuilder, "from_config") as from_config_mock:
        from_config_mock.return_value = command_builder3
        commands_repository.update_from_config({COMMAND3: builder_config})
        from_config_mock.assert_called_once_with(
            command_name=COMMAND3, builder_setups=builder_config
        )

    assert len(commands_repository) == 3
    assert commands_repository[COMMAND1] == command_builder1
    assert commands_repository[COMMAND2] == command_builder2
    assert commands_repository[COMMAND3] == command_builder3


def test_commands_repository_updates_existing_builder():
    command_builder1, command_builder2 = (
        command_builder_mock(name=COMMAND1),
        command_builder_mock(name=COMMAND2),
    )
    builder_config = mock.Mock()
    commands_repository = CommandsRepository()
    commands_repository.add_command_builders(command_builder1, command_builder2)

    commands_repository.update_from_config({COMMAND1: builder_config})
    command_builder1.update_from_config.assert_called_once_with(builder_config)

    assert len(commands_repository) == 2
    assert commands_repository[COMMAND1] == command_builder1
    assert commands_repository[COMMAND2] == command_builder2
