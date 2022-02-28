from pathlib import Path
from typing import Any, Dict

import pytest

from statue.commands_filter import CommandsFilter
from statue.configuration import Configuration
from statue.constants import CONTEXTS, SOURCES
from statue.context import Context
from statue.exceptions import MissingConfiguration
from tests.constants import (
    CONTEXT1,
    CONTEXT_HELP_STRING1,
    NOT_EXISTING_SOURCE,
    SOURCE1,
    SOURCE2,
    SOURCE3,
)

SOURCES_CONFIGURATION: Dict[str, Any] = {
    SOURCE1: {CONTEXTS: [CONTEXT1]},
    SOURCE2: {},
    SOURCE3: {},
}


def test_simple_sources_configuration(clear_configuration):
    Configuration.contexts_repository.add_contexts(
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    )
    Configuration.set_statue_configuration({SOURCES: SOURCES_CONFIGURATION})
    assert (
        Configuration.sources_configuration() == SOURCES_CONFIGURATION
    ), "Sources configuration is different than expected"
    assert Configuration.sources_list() == [
        SOURCE1,
        SOURCE2,
        SOURCE3,
    ], "Sources list is different than expected"


def test_empty_sources_configuration(clear_configuration):
    Configuration.set_statue_configuration({})
    with pytest.raises(
        MissingConfiguration,
        match=f'^"{SOURCES}" is missing from Statue configuration.$',
    ):
        Configuration.sources_configuration()


def test_non_existing_sources_configuration_raises_exception(clear_configuration):
    Configuration.set_statue_configuration({})
    with pytest.raises(
        MissingConfiguration,
        match=f'^"{SOURCES}" is missing from Statue configuration.$',
    ):
        Configuration.get_source_commands_filter(SOURCE1)


def test_get_source_as_string(clear_configuration):
    context = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    Configuration.contexts_repository.add_contexts(context)
    Configuration.set_statue_configuration({SOURCES: SOURCES_CONFIGURATION})
    commands_filter = Configuration.get_source_commands_filter(SOURCE1)
    assert commands_filter == CommandsFilter(
        contexts=[context]
    ), "Source commands filter is different than expected"


def test_get_source_as_path(clear_configuration):
    context = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    Configuration.contexts_repository.add_contexts(context)
    Configuration.set_statue_configuration({SOURCES: SOURCES_CONFIGURATION})
    commands_filter = Configuration.get_source_commands_filter(Path(SOURCE1))
    assert commands_filter == CommandsFilter(
        contexts=[context]
    ), "Source commands filter is different than expected"


def test_get_non_existing_source(clear_configuration):
    context = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    Configuration.contexts_repository.add_contexts(context)
    Configuration.set_statue_configuration({SOURCES: SOURCES_CONFIGURATION})
    commands_filter = Configuration.get_source_commands_filter(NOT_EXISTING_SOURCE)
    assert (
        commands_filter == CommandsFilter()
    ), "Source commands filter is different than expected"
