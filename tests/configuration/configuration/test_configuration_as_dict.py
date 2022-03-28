from collections import OrderedDict

import mock
import pytest

from statue.config.configuration import Configuration
from statue.constants import COMMANDS, CONTEXTS, GENERAL, MODE, SOURCES
from statue.runner import RunnerMode


def test_configuration_as_dict_default(
    mock_contexts_repository_as_dict,
    mock_commands_repository_as_dict,
    mock_sources_repository_as_dict,
):
    configuration = Configuration(cache=mock.Mock())
    configuration_dict = configuration.as_dict()

    assert isinstance(configuration_dict, OrderedDict)
    assert list(configuration_dict.keys()) == [GENERAL, CONTEXTS, COMMANDS, SOURCES]
    assert configuration_dict[GENERAL] == {MODE: "sync"}
    assert configuration_dict[CONTEXTS] == mock_contexts_repository_as_dict.return_value
    assert configuration_dict[COMMANDS] == mock_commands_repository_as_dict.return_value
    assert configuration_dict[SOURCES] == mock_sources_repository_as_dict.return_value


@pytest.mark.parametrize(argnames="mode", argvalues=[RunnerMode.SYNC, RunnerMode.ASYNC])
def test_configuration_as_dict_with_runner_mode(
    mode,
    mock_contexts_repository_as_dict,
    mock_commands_repository_as_dict,
    mock_sources_repository_as_dict,
):
    configuration = Configuration(cache=mock.Mock(), default_mode=mode)
    configuration_dict = configuration.as_dict()

    assert isinstance(configuration_dict, OrderedDict)
    assert list(configuration_dict.keys()) == [GENERAL, CONTEXTS, COMMANDS, SOURCES]
    assert configuration_dict[GENERAL] == {MODE: mode.name.lower()}
    assert configuration_dict[CONTEXTS] == mock_contexts_repository_as_dict.return_value
    assert configuration_dict[COMMANDS] == mock_commands_repository_as_dict.return_value
    assert configuration_dict[SOURCES] == mock_sources_repository_as_dict.return_value
