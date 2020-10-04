from typing import Any, Dict

import pytest

from statue.configuration import Configuration
from statue.constants import SOURCES
from statue.exceptions import MissingConfiguration
from tests.constants import SOURCE1, SOURCE2, SOURCE3

SOURCES_CONFIGURATION: Dict[str, Any] = {SOURCE1: {}, SOURCE2: {}, SOURCE3: {}}


def test_simple_sources_configuration(clear_configuration):
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
    assert (
        Configuration.sources_configuration() is None
    ), "Sources configuration is different than expected"
    assert Configuration.sources_list() == [], "Sources list is different than expected"


def test_non_existing_sources_configuration_raises_exception(clear_configuration):
    Configuration.set_statue_configuration({})
    with pytest.raises(
        MissingConfiguration,
        match=f'^"{SOURCES}" is missing from Statue configuration.$',
    ):
        Configuration.get_source_configuration(SOURCE1)
