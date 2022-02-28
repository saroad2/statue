from pathlib import Path

from statue.commands_filter import CommandsFilter
from statue.context import Context
from statue.sources_repository import SourcesRepository
from tests.constants import (
    COMMAND1,
    COMMAND2,
    COMMAND3,
    COMMAND4,
    CONTEXT1,
    CONTEXT2,
    CONTEXT_HELP_STRING1,
    CONTEXT_HELP_STRING2,
    SOURCE1,
    SOURCE2,
    SOURCE3,
)


def test_sources_repository_constructor():
    sources_repository = SourcesRepository()

    assert not sources_repository.sources_list
    assert len(sources_repository) == 0


def test_sources_repository_add_one_filter():
    sources_repository = SourcesRepository()
    commands_filter = CommandsFilter(
        contexts=[Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)],
        allowed_commands=[COMMAND1, COMMAND2],
    )
    sources_repository[Path(SOURCE1)] = commands_filter

    assert len(sources_repository) == 1
    assert sources_repository.sources_list == [Path(SOURCE1)]
    assert sources_repository[Path(SOURCE1)] == commands_filter


def test_sources_repository_add_multiple_filters():
    sources_repository = SourcesRepository()
    commands_filter1, commands_filter2, commands_filter3 = (
        CommandsFilter(
            contexts=[Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)],
            allowed_commands=[COMMAND1, COMMAND2],
        ),
        CommandsFilter(contexts=[Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2)]),
        CommandsFilter(denied_commands=[COMMAND3, COMMAND4]),
    )
    sources_repository[Path(SOURCE1)] = commands_filter1
    sources_repository[Path(SOURCE2)] = commands_filter2
    sources_repository[Path(SOURCE3)] = commands_filter3

    assert len(sources_repository) == 3
    assert sources_repository.sources_list == [
        Path(SOURCE1),
        Path(SOURCE2),
        Path(SOURCE3),
    ]
    assert sources_repository[Path(SOURCE1)] == commands_filter1
    assert sources_repository[Path(SOURCE2)] == commands_filter2
    assert sources_repository[Path(SOURCE3)] == commands_filter3


def test_sources_repository_child_source_gets_parent_filter():
    sources_repository = SourcesRepository()
    commands_filter1, commands_filter2 = (
        CommandsFilter(
            contexts=[Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)],
            allowed_commands=[COMMAND1, COMMAND2],
        ),
        CommandsFilter(contexts=[Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2)]),
    )
    sources_repository[Path(SOURCE1)] = commands_filter1
    sources_repository[Path(SOURCE2)] = commands_filter2

    assert len(sources_repository) == 2
    assert sources_repository.sources_list == [Path(SOURCE1), Path(SOURCE2)]
    assert sources_repository[Path(SOURCE1)] == commands_filter1
    assert sources_repository[Path(SOURCE2)] == commands_filter2
    assert sources_repository[Path(SOURCE1) / SOURCE3] == commands_filter1


def test_sources_repository_get_filter_of_unknown_source():
    sources_repository = SourcesRepository()
    sources_repository[Path(SOURCE1)] = CommandsFilter(
        contexts=[Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)],
        allowed_commands=[COMMAND1, COMMAND2],
    )

    assert sources_repository[Path(SOURCE2)] == CommandsFilter()


def test_sources_repository_reset():
    sources_repository = SourcesRepository()
    sources_repository[Path(SOURCE1)] = CommandsFilter(
        contexts=[Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)],
        allowed_commands=[COMMAND1, COMMAND2],
    )
    sources_repository[Path(SOURCE2)] = CommandsFilter(
        contexts=[Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2)]
    )
    sources_repository[Path(SOURCE3)] = CommandsFilter(
        denied_commands=[COMMAND3, COMMAND4]
    )

    sources_repository.reset()

    assert len(sources_repository) == 0
    assert not sources_repository.sources_list
