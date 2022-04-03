import mock

from statue.command_builder import CommandBuilder
from statue.config.commands_repository import CommandsRepository
from statue.config.contexts_repository import ContextsRepository
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
    contexts_repository = ContextsRepository()

    commands_repository.update_from_config(
        config={}, contexts_repository=contexts_repository
    )

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
    contexts_repository = ContextsRepository()

    with mock.patch.object(CommandBuilder, "from_dict") as from_dict_mock:
        from_dict_mock.return_value = command_builder3
        commands_repository.update_from_config(
            config={COMMAND3: builder_config}, contexts_repository=contexts_repository
        )
        from_dict_mock.assert_called_once_with(
            command_name=COMMAND3,
            builder_setups=builder_config,
            contexts_repository=contexts_repository,
        )

    assert len(commands_repository) == 3
    assert commands_repository[COMMAND1] == command_builder1
    assert commands_repository[COMMAND2] == command_builder2
    assert commands_repository[COMMAND3] == command_builder3
