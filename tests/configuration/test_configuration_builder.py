import mock
import pytest

from statue.config.commands_repository import CommandsRepository
from statue.config.configuration_builder import ConfigurationBuilder
from statue.config.contexts_repository import ContextsRepository
from statue.config.sources_repository import SourcesRepository
from statue.constants import COMMANDS, CONTEXTS, OVERRIDE, SOURCES
from statue.exceptions import MissingConfiguration


@pytest.fixture
def mock_contexts_repository_update_from_config(mocker):
    return mocker.patch.object(ContextsRepository, "update_from_config")


@pytest.fixture
def mock_sources_repository_update_from_config(mocker):
    return mocker.patch.object(SourcesRepository, "update_from_config")


@pytest.fixture
def mock_commands_repository_update_from_config(mocker):
    return mocker.patch.object(CommandsRepository, "update_from_config")


@pytest.fixture
def mock_default_configuration_path(mocker):
    default_path = mocker.patch.object(
        ConfigurationBuilder, "default_configuration_path"
    )
    default_path.return_value.exists.return_value = True
    return default_path


@pytest.fixture
def mock_configuration_path(mocker):
    return mocker.patch.object(ConfigurationBuilder, "configuration_path")


def test_configuration_builder_configuration_path(tmp_path):
    assert ConfigurationBuilder.configuration_path(tmp_path) == tmp_path / "statue.toml"


def test_configuration_builder_default_path():
    assert ConfigurationBuilder.default_configuration_path().exists()


def test_load_configuration_from_file_with_override(
    mock_toml_load,
    mock_contexts_repository_update_from_config,
    mock_sources_repository_update_from_config,
    mock_commands_repository_update_from_config,
):
    new_contexts_config, new_sources_config, new_commands_config = (
        mock.Mock(),
        mock.Mock(),
        mock.Mock(),
    )
    mock_toml_load.return_value = {
        OVERRIDE: True,
        CONTEXTS: new_contexts_config,
        SOURCES: new_sources_config,
        COMMANDS: new_commands_config,
    }
    configuration_path = mock.Mock()
    configuration_path.exists.return_value = True

    configuration = ConfigurationBuilder.build_configuration_from_file(
        configuration_path
    )
    mock_toml_load.assert_called_once_with(configuration_path)
    mock_contexts_repository_update_from_config.assert_called_once_with(
        new_contexts_config
    )
    mock_sources_repository_update_from_config.assert_called_once_with(
        config=new_sources_config, contexts_repository=configuration.contexts_repository
    )
    mock_commands_repository_update_from_config.assert_called_once_with(
        new_commands_config
    )


def test_load_configuration_from_file_without_override(
    mock_toml_load,
    mock_default_configuration_path,
    mock_contexts_repository_update_from_config,
    mock_sources_repository_update_from_config,
    mock_commands_repository_update_from_config,
):
    default_contexts_config, default_sources_config, default_commands_config = (
        mock.Mock(),
        mock.Mock(),
        mock.Mock(),
    )
    new_contexts_config, new_sources_config, new_commands_config = (
        mock.Mock(),
        mock.Mock(),
        mock.Mock(),
    )
    new_config = {
        CONTEXTS: new_contexts_config,
        SOURCES: new_sources_config,
        COMMANDS: new_commands_config,
    }
    default_config = {
        CONTEXTS: default_contexts_config,
        SOURCES: default_sources_config,
        COMMANDS: default_commands_config,
    }
    mock_toml_load.side_effect = [new_config, default_config]
    configuration_path = mock.Mock()
    configuration_path.exists.return_value = True

    configuration = ConfigurationBuilder.build_configuration_from_file(
        configuration_path
    )
    assert mock_toml_load.call_count == 2
    assert mock_toml_load.call_args_list == [
        mock.call(configuration_path),
        mock.call(mock_default_configuration_path.return_value),
    ]
    assert mock_contexts_repository_update_from_config.call_count == 2
    assert mock_contexts_repository_update_from_config.call_args_list == [
        mock.call(default_contexts_config),
        mock.call(new_contexts_config),
    ]
    assert mock_sources_repository_update_from_config.call_count == 2
    assert mock_sources_repository_update_from_config.call_args_list == [
        mock.call(
            config=default_sources_config,
            contexts_repository=configuration.contexts_repository,
        ),
        mock.call(
            config=new_sources_config,
            contexts_repository=configuration.contexts_repository,
        ),
    ]
    assert mock_commands_repository_update_from_config.call_count == 2
    assert mock_commands_repository_update_from_config.call_args_list == [
        mock.call(default_commands_config),
        mock.call(new_commands_config),
    ]


def test_load_configuration_from_file_with_cwd_file(  # pylint: disable=too-many-locals
    mock_cwd,
    mock_toml_load,
    mock_configuration_path,
    mock_default_configuration_path,
    mock_contexts_repository_update_from_config,
    mock_sources_repository_update_from_config,
    mock_commands_repository_update_from_config,
):
    default_contexts_config, default_sources_config, default_commands_config = (
        mock.Mock(),
        mock.Mock(),
        mock.Mock(),
    )
    new_contexts_config, new_sources_config, new_commands_config = (
        mock.Mock(),
        mock.Mock(),
        mock.Mock(),
    )
    new_config = {
        CONTEXTS: new_contexts_config,
        SOURCES: new_sources_config,
        COMMANDS: new_commands_config,
    }
    default_config = {
        CONTEXTS: default_contexts_config,
        SOURCES: default_sources_config,
        COMMANDS: default_commands_config,
    }
    mock_toml_load.side_effect = [new_config, default_config]
    configuration_path = mock_configuration_path.return_value
    configuration_path.exists.return_value = True

    configuration = ConfigurationBuilder.build_configuration_from_file()
    mock_configuration_path.assert_called_once_with(mock_cwd)
    assert mock_toml_load.call_count == 2
    assert mock_toml_load.call_args_list == [
        mock.call(configuration_path),
        mock.call(mock_default_configuration_path.return_value),
    ]
    assert mock_contexts_repository_update_from_config.call_count == 2
    assert mock_contexts_repository_update_from_config.call_args_list == [
        mock.call(default_contexts_config),
        mock.call(new_contexts_config),
    ]
    assert mock_sources_repository_update_from_config.call_count == 2
    assert mock_sources_repository_update_from_config.call_args_list == [
        mock.call(
            config=default_sources_config,
            contexts_repository=configuration.contexts_repository,
        ),
        mock.call(
            config=new_sources_config,
            contexts_repository=configuration.contexts_repository,
        ),
    ]
    assert mock_commands_repository_update_from_config.call_count == 2
    assert mock_commands_repository_update_from_config.call_args_list == [
        mock.call(default_commands_config),
        mock.call(new_commands_config),
    ]


def test_load_configuration_from_non_existing_file(
    mock_toml_load,
    mock_default_configuration_path,
    mock_contexts_repository_update_from_config,
    mock_sources_repository_update_from_config,
    mock_commands_repository_update_from_config,
):
    default_contexts_config, default_sources_config, default_commands_config = (
        mock.Mock(),
        mock.Mock(),
        mock.Mock(),
    )
    mock_toml_load.return_value = {
        OVERRIDE: True,
        CONTEXTS: default_contexts_config,
        SOURCES: default_sources_config,
        COMMANDS: default_commands_config,
    }
    configuration_path = mock.Mock()
    configuration_path.exists.return_value = False

    configuration = ConfigurationBuilder.build_configuration_from_file(
        configuration_path
    )
    mock_toml_load.assert_called_once_with(mock_default_configuration_path.return_value)
    mock_contexts_repository_update_from_config.assert_called_once_with(
        default_contexts_config
    )
    mock_sources_repository_update_from_config.assert_called_once_with(
        config=default_sources_config,
        contexts_repository=configuration.contexts_repository,
    )
    mock_commands_repository_update_from_config.assert_called_once_with(
        default_commands_config
    )


def test_load_configuration_raises_missing_configuration(
    mock_toml_load,
    mock_default_configuration_path,
    mock_contexts_repository_update_from_config,
    mock_sources_repository_update_from_config,
    mock_commands_repository_update_from_config,
):
    configuration_path = mock.Mock()
    configuration_path.exists.return_value = False
    mock_default_configuration_path.return_value.exists.return_value = False

    with pytest.raises(
        MissingConfiguration, match="^Statue was unable to load configuration$"
    ):
        ConfigurationBuilder.build_configuration_from_file(configuration_path)
