import mock

from statue.commands_filter import CommandsFilter
from statue.config.configuration import Configuration
from tests.constants import COMMAND1, COMMAND2, SOURCE1


def test_configuration_remove_context_from_contexts_configuration():
    context = mock.Mock()
    configuration = Configuration(cache=mock.Mock())
    configuration.contexts_repository = mock.MagicMock()

    configuration.remove_context(context)

    configuration.contexts_repository.remove_context.assert_called_once_with(context)


def test_configuration_remove_context_from_command_builders():
    context = mock.Mock()
    command_builder1, command_builder2, command_builder3 = (
        mock.Mock(),
        mock.Mock(),
        mock.Mock(),
    )
    configuration = Configuration(cache=mock.Mock())
    configuration.contexts_repository = mock.MagicMock()
    configuration.commands_repository.add_command_builders(
        command_builder1, command_builder2, command_builder3
    )

    configuration.remove_context(context)

    command_builder1.remove_context.assert_called_once_with(context)
    command_builder2.remove_context.assert_called_once_with(context)
    command_builder3.remove_context.assert_called_once_with(context)


def test_configuration_remove_context_from_source(tmp_path):
    context1, context2, context3 = mock.Mock(), mock.Mock(), mock.Mock()
    configuration = Configuration(cache=mock.Mock())
    configuration.contexts_repository = mock.MagicMock()
    configuration.sources_repository[tmp_path / SOURCE1] = CommandsFilter(
        contexts=[context1, context2, context3], allowed_commands=[COMMAND1, COMMAND2]
    )

    configuration.remove_context(context2)

    assert configuration.sources_repository[tmp_path / SOURCE1] == CommandsFilter(
        contexts=[context1, context3], allowed_commands=[COMMAND1, COMMAND2]
    )
