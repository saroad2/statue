import mock
import pytest

from statue.cli import statue_cli
from statue.cli.config.interactive_adders.interactive_context_adder import (
    InteractiveContextAdder,
)
from statue.exceptions import UnknownContext
from tests.constants import CONTEXT1


def test_config_add_context_with_default_path(
    cli_runner, mock_build_configuration_from_file, mock_configuration_path
):
    configuration = mock_build_configuration_from_file.return_value
    with mock.patch.object(InteractiveContextAdder, "add_context") as mock_add_context:
        result = cli_runner.invoke(statue_cli, ["config", "add-context"])
        mock_add_context.assert_called_once_with(configuration.contexts_repository)

    mock_build_configuration_from_file.assert_called_once_with(
        mock_configuration_path.return_value
    )
    assert result.exit_code == 0


def test_config_add_context_with_path(
    cli_runner, mock_build_configuration_from_file, mock_configuration_path, tmp_path
):
    config_path = tmp_path / "statue.toml"
    config_path.touch()
    configuration = mock_build_configuration_from_file.return_value
    with mock.patch.object(InteractiveContextAdder, "add_context") as mock_add_context:
        result = cli_runner.invoke(
            statue_cli, ["config", "add-context", "--config", str(config_path)]
        )
        mock_add_context.assert_called_once_with(configuration.contexts_repository)

    mock_build_configuration_from_file.assert_called_once_with(config_path)
    mock_configuration_path.assert_not_called()
    assert result.exit_code == 0


def test_config_edit_context_with_default_path(
    cli_runner, mock_build_configuration_from_file, mock_configuration_path
):
    configuration = mock_build_configuration_from_file.return_value
    with mock.patch.object(
        InteractiveContextAdder, "edit_context"
    ) as mock_edit_context:
        result = cli_runner.invoke(statue_cli, ["config", "edit-context", CONTEXT1])
        mock_edit_context.assert_called_once_with(
            name=CONTEXT1, contexts_repository=configuration.contexts_repository
        )

    mock_build_configuration_from_file.assert_called_once_with(
        mock_configuration_path.return_value
    )
    assert result.exit_code == 0


def test_config_edit_context_with_path(
    cli_runner, mock_build_configuration_from_file, mock_configuration_path, tmp_path
):
    config_path = tmp_path / "statue.toml"
    config_path.touch()
    configuration = mock_build_configuration_from_file.return_value
    with mock.patch.object(
        InteractiveContextAdder, "edit_context"
    ) as mock_edit_context:
        result = cli_runner.invoke(
            statue_cli,
            ["config", "edit-context", CONTEXT1, "--config", str(config_path)],
        )
        mock_edit_context.assert_called_once_with(
            name=CONTEXT1, contexts_repository=configuration.contexts_repository
        )

    mock_build_configuration_from_file.assert_called_once_with(config_path)
    mock_configuration_path.assert_not_called()
    assert result.exit_code == 0


def test_config_remove_context_with_default_path(
    cli_runner, mock_build_configuration_from_file, mock_configuration_path
):
    mock_build_configuration_from_file.return_value = configuration = mock.MagicMock()
    context = configuration.contexts_repository.__getitem__.return_value
    result = cli_runner.invoke(
        statue_cli, ["config", "remove-context", CONTEXT1], input="y\n"
    )
    configuration.contexts_repository.__getitem__.assert_called_once_with(CONTEXT1)
    configuration.remove_context.assert_called_once_with(context)

    mock_build_configuration_from_file.assert_called_once_with(
        mock_configuration_path.return_value
    )
    assert result.exit_code == 0


def test_config_remove_context_with_path(
    cli_runner, mock_build_configuration_from_file, mock_configuration_path, tmp_path
):
    config_path = tmp_path / "statue.toml"
    config_path.touch()
    mock_build_configuration_from_file.return_value = configuration = mock.MagicMock()
    context = configuration.contexts_repository.__getitem__.return_value
    result = cli_runner.invoke(
        statue_cli,
        ["config", "remove-context", CONTEXT1, "--config", str(config_path)],
        input="y\n",
    )
    configuration.contexts_repository.__getitem__.assert_called_once_with(CONTEXT1)
    configuration.remove_context.assert_called_once_with(context)

    mock_build_configuration_from_file.assert_called_once_with(config_path)
    mock_configuration_path.assert_not_called()
    assert result.exit_code == 0


def test_config_remove_unknown_context_fails(
    cli_runner, mock_build_configuration_from_file, mock_configuration_path, tmp_path
):
    config_path = tmp_path / "statue.toml"
    config_path.touch()
    mock_build_configuration_from_file.return_value = configuration = mock.MagicMock()
    configuration.contexts_repository.__getitem__.side_effect = UnknownContext(CONTEXT1)
    result = cli_runner.invoke(
        statue_cli,
        ["config", "remove-context", CONTEXT1, "--config", str(config_path)],
    )

    assert result.exit_code == 1
    assert result.output == f'Could not find context named "{CONTEXT1}"\n'


@pytest.mark.parametrize(argnames="abort_flag", argvalues=["", "n"])
def test_config_remove_context_abort(
    abort_flag, cli_runner, mock_build_configuration_from_file, mock_configuration_path
):
    mock_build_configuration_from_file.return_value = configuration = mock.MagicMock()
    result = cli_runner.invoke(
        statue_cli, ["config", "remove-context", CONTEXT1], input=f"{abort_flag}\n"
    )
    configuration.contexts_repository.__getitem__.assert_called_once_with(CONTEXT1)
    configuration.remove_context.assert_not_called()

    mock_build_configuration_from_file.assert_called_once_with(
        mock_configuration_path.return_value
    )
    assert result.exit_code == 0
    assert result.output == (
        "Are you sure you would like to remove the context context1 and all of its "
        f"references from configuration? [y/N]: {abort_flag}\n"
        "Abort!\n"
    )
