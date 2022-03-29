import mock

from statue.cli import statue_cli
from statue.cli.config.interactive_adders.interactive_context_adder import (
    InteractiveContextAdder,
)
from tests.constants import CONTEXT1


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
