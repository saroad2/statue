from pathlib import Path

from statue.commands_filter import CommandsFilter
from statue.config.contexts_repository import ContextsRepository
from statue.config.sources_repository import SourcesRepository
from statue.constants import ALLOW_LIST, CONTEXTS, DENY_LIST
from statue.context import Context
from tests.constants import (
    COMMAND1,
    COMMAND2,
    CONTEXT1,
    CONTEXT2,
    CONTEXT_HELP_STRING1,
    CONTEXT_HELP_STRING2,
    SOURCE1,
    SOURCE2,
)


def test_sources_repository_from_empty_dict():
    sources_repository = SourcesRepository.from_dict(
        config={}, contexts_repository=ContextsRepository()
    )

    assert len(sources_repository) == 0


def test_sources_repository_from_dict_source_with_empty_configuration():
    sources_repository = SourcesRepository.from_dict(
        config={SOURCE1: {}}, contexts_repository=ContextsRepository()
    )

    assert len(sources_repository) == 1
    assert sources_repository[Path(SOURCE1)] == CommandsFilter()


def test_sources_repository_from_dict_source_with_contexts():
    context1, context2 = (
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1),
        Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2),
    )

    sources_repository = SourcesRepository.from_dict(
        config={SOURCE1: {CONTEXTS: [CONTEXT1, CONTEXT2]}},
        contexts_repository=ContextsRepository(context1, context2),
    )

    assert len(sources_repository) == 1
    assert sources_repository[Path(SOURCE1)] == CommandsFilter(
        contexts=[context1, context2]
    )


def test_sources_repository_from_dict_source_with_allowed_commands():
    sources_repository = SourcesRepository.from_dict(
        config={SOURCE1: {ALLOW_LIST: [COMMAND1, COMMAND2]}},
        contexts_repository=ContextsRepository(),
    )

    assert len(sources_repository) == 1
    assert sources_repository[Path(SOURCE1)] == CommandsFilter(
        allowed_commands=[COMMAND1, COMMAND2]
    )


def test_sources_repository_from_dict_source_with_denied_commands():
    sources_repository = SourcesRepository.from_dict(
        config={SOURCE1: {DENY_LIST: [COMMAND1, COMMAND2]}},
        contexts_repository=ContextsRepository(),
    )

    assert len(sources_repository) == 1
    assert sources_repository[Path(SOURCE1)] == CommandsFilter(
        denied_commands=[COMMAND1, COMMAND2]
    )


def test_sources_repository_from_dict_multiple_sources():
    context1, context2 = (
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1),
        Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2),
    )

    sources_repository = SourcesRepository.from_dict(
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
