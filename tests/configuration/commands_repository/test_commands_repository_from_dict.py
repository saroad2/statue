from collections import OrderedDict

import mock

from statue.command_builder import CommandBuilder
from statue.config.commands_repository import CommandsRepository
from statue.config.contexts_repository import ContextsRepository
from tests.constants import COMMAND1, COMMAND2, COMMAND3
from tests.util import command_builder_mock


def test_commands_repository_update_from_empty_config():
    contexts_repository = ContextsRepository()
    commands_repository = CommandsRepository.from_dict(
        config={}, contexts_repository=contexts_repository
    )

    assert len(commands_repository) == 0


def test_commands_repository_update_with_three_builder():
    command_builder1, command_builder2, command_builder3 = (
        command_builder_mock(name=COMMAND1),
        command_builder_mock(name=COMMAND2),
        command_builder_mock(name=COMMAND3),
    )
    builder_config1, builder_config2, builder_config3 = (
        mock.Mock(),
        mock.Mock(),
        mock.Mock(),
    )
    contexts_repository = ContextsRepository()

    with mock.patch.object(CommandBuilder, "from_dict") as from_dict_mock:
        from_dict_mock.side_effect = [
            command_builder1,
            command_builder2,
            command_builder3,
        ]
        commands_repository = CommandsRepository.from_dict(
            config=OrderedDict(
                [
                    (COMMAND1, builder_config1),
                    (COMMAND2, builder_config2),
                    (COMMAND3, builder_config3),
                ]
            ),
            contexts_repository=contexts_repository,
        )
        assert from_dict_mock.call_count == 3
        assert from_dict_mock.call_args_list == [
            mock.call(
                command_name=COMMAND1,
                builder_setups=builder_config1,
                contexts_repository=contexts_repository,
            ),
            mock.call(
                command_name=COMMAND2,
                builder_setups=builder_config2,
                contexts_repository=contexts_repository,
            ),
            mock.call(
                command_name=COMMAND3,
                builder_setups=builder_config3,
                contexts_repository=contexts_repository,
            ),
        ]

    assert len(commands_repository) == 3
    assert commands_repository[COMMAND1] == command_builder1
    assert commands_repository[COMMAND2] == command_builder2
    assert commands_repository[COMMAND3] == command_builder3
