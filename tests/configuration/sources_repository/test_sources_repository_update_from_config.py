from pathlib import Path

from statue.commands_filter import CommandsFilter
from statue.config.contexts_repository import ContextsRepository
from statue.config.sources_repository import SourcesRepository
from statue.constants import ALLOW_LIST, CONTEXTS, DENY_LIST
from statue.context import Context
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


def test_sources_repository_update_from_empty_config():
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

    sources_repository.update_from_config(
        config={}, contexts_repository=ContextsRepository()
    )

    assert len(sources_repository) == 3
    assert sources_repository[Path(SOURCE1)] == commands_filter1
    assert sources_repository[Path(SOURCE2)] == commands_filter2
    assert sources_repository[Path(SOURCE3)] == commands_filter3


def test_sources_repository_update_adds_source_with_empty_configuration():
    sources_repository = SourcesRepository()

    sources_repository.update_from_config(
        config={SOURCE1: {}}, contexts_repository=ContextsRepository()
    )

    assert len(sources_repository) == 1
    assert sources_repository[Path(SOURCE1)] == CommandsFilter()


def test_sources_repository_update_adds_source_with_contexts():
    sources_repository = SourcesRepository()
    context1, context2 = (
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1),
        Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2),
    )

    sources_repository.update_from_config(
        config={SOURCE1: {CONTEXTS: [CONTEXT1, CONTEXT2]}},
        contexts_repository=ContextsRepository(context1, context2),
    )

    assert len(sources_repository) == 1
    assert sources_repository[Path(SOURCE1)] == CommandsFilter(
        contexts=[context1, context2]
    )


def test_sources_repository_update_adds_source_with_allowed_commands():
    sources_repository = SourcesRepository()

    sources_repository.update_from_config(
        config={SOURCE1: {ALLOW_LIST: [COMMAND1, COMMAND2]}},
        contexts_repository=ContextsRepository(),
    )

    assert len(sources_repository) == 1
    assert sources_repository[Path(SOURCE1)] == CommandsFilter(
        allowed_commands=[COMMAND1, COMMAND2]
    )


def test_sources_repository_update_adds_source_with_denied_commands():
    sources_repository = SourcesRepository()

    sources_repository.update_from_config(
        config={SOURCE1: {DENY_LIST: [COMMAND1, COMMAND2]}},
        contexts_repository=ContextsRepository(),
    )

    assert len(sources_repository) == 1
    assert sources_repository[Path(SOURCE1)] == CommandsFilter(
        denied_commands=[COMMAND1, COMMAND2]
    )


def test_sources_repository_update_override_source():
    sources_repository = SourcesRepository()
    sources_repository[Path(SOURCE1)] = CommandsFilter(
        contexts=[Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)],
        allowed_commands=[COMMAND3],
    )

    sources_repository.update_from_config(
        config={SOURCE1: {DENY_LIST: [COMMAND1, COMMAND2]}},
        contexts_repository=ContextsRepository(),
    )

    assert len(sources_repository) == 1
    assert sources_repository[Path(SOURCE1)] == CommandsFilter(
        denied_commands=[COMMAND1, COMMAND2]
    )


def test_sources_repository_update_adds_multiple_sources():
    sources_repository = SourcesRepository()
    context1, context2 = (
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1),
        Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2),
    )

    sources_repository.update_from_config(
        config={
            SOURCE1: {CONTEXTS: [CONTEXT1], DENY_LIST: [COMMAND1]},
            SOURCE2: {CONTEXTS: [CONTEXT1, CONTEXT2], ALLOW_LIST: [COMMAND2]},
        },
        contexts_repository=ContextsRepository(context1, context2),
    )

    assert len(sources_repository) == 2
    assert sources_repository[Path(SOURCE1)] == CommandsFilter(
        contexts=[context1], denied_commands=[COMMAND1]
    )
    assert sources_repository[Path(SOURCE2)] == CommandsFilter(
        contexts=[context1, context2], allowed_commands=[COMMAND2]
    )
