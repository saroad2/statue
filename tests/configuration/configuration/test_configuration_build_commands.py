import mock

from statue.config.configuration import Configuration
from tests.constants import COMMAND1, COMMAND2, COMMAND3, CONTEXT1, CONTEXT2
from tests.util import command_builder_mock


def test_build_commands_from_empty_list():
    commands_filter = mock.Mock()
    configuration = Configuration(cache=mock.Mock())
    commands = configuration.build_commands(commands_filter=commands_filter)

    assert commands == []


def test_build_commands_with_one_command_builder_passing_filter():
    command_builder = command_builder_mock(name=COMMAND1)
    configuration = Configuration(cache=mock.Mock())
    configuration.commands_repository.add_command_builders(command_builder)
    commands_filter = mock.Mock()
    commands_filter.contexts = [CONTEXT1, CONTEXT2]
    commands_filter.pass_filter.return_value = True
    commands = configuration.build_commands(commands_filter=commands_filter)

    assert commands == [command_builder.build_command.return_value]
    command_builder.build_command.assert_called_once_with(CONTEXT1, CONTEXT2)


def test_build_commands_with_one_command_builder_not_passing_filter():
    command_builder = command_builder_mock(name=COMMAND1)
    configuration = Configuration(cache=mock.Mock())
    configuration.commands_repository.add_command_builders(command_builder)
    commands_filter = mock.Mock()
    commands_filter.contexts = [CONTEXT1, CONTEXT2]
    commands_filter.pass_filter.return_value = False
    commands = configuration.build_commands(commands_filter=commands_filter)

    assert commands == []
    command_builder.build_command.assert_not_called()


def test_build_commands_with_few_passing_command_builders():
    command_builder1, command_builder2, command_builder3 = (
        command_builder_mock(name=COMMAND1),
        command_builder_mock(name=COMMAND2),
        command_builder_mock(name=COMMAND3),
    )
    configuration = Configuration(cache=mock.Mock())
    configuration.commands_repository.add_command_builders(
        command_builder1, command_builder2, command_builder3
    )
    commands_filter = mock.Mock()
    commands_filter.contexts = [CONTEXT1, CONTEXT2]
    commands_filter.pass_filter.side_effect = [True, False, True]
    commands = configuration.build_commands(commands_filter=commands_filter)

    assert commands == [
        command_builder1.build_command.return_value,
        command_builder3.build_command.return_value,
    ]

    command_builder1.build_command.assert_called_once_with(CONTEXT1, CONTEXT2)
    command_builder2.build_command.assert_not_called()
    command_builder3.build_command.assert_called_once_with(CONTEXT1, CONTEXT2)
