import pytest

from statue.cli import statue_cli


def test_templates_clear_successful(
    cli_runner,
    mock_templates_provider_user_names,
    mock_templates_provider_clear_user_templates,
):
    mock_templates_provider_user_names.return_value = ["a", "b", "c"]

    result = cli_runner.invoke(statue_cli, ["templates", "clear"], input="y\n")

    assert result.exit_code == 0
    assert result.output == (
        "Are you sure you want to remove 3 templates? [y/N]: y\n"
        "All user templates were successfully remove!\n"
    )
    mock_templates_provider_clear_user_templates.assert_called_once_with()


def test_templates_clear_successful_no_user_templates(
    cli_runner,
    mock_templates_provider_user_names,
    mock_templates_provider_clear_user_templates,
):
    mock_templates_provider_user_names.return_value = []

    result = cli_runner.invoke(statue_cli, ["templates", "clear"])

    assert result.exit_code == 0
    assert result.output == "No templates to remove.\n"
    mock_templates_provider_clear_user_templates.assert_not_called()


@pytest.mark.parametrize("confirmation_response", ["", "n", "N"])
def test_templates_clear_no_confirmation(
    cli_runner,
    confirmation_response,
    mock_templates_provider_user_names,
    mock_templates_provider_clear_user_templates,
):
    mock_templates_provider_user_names.return_value = ["a", "b", "c"]

    result = cli_runner.invoke(
        statue_cli, ["templates", "clear"], input=f"{confirmation_response}\n"
    )

    assert result.exit_code == 1
    assert result.output == (
        f"Are you sure you want to remove 3 templates? [y/N]: {confirmation_response}\n"
        "Abort!\n"
    )
    mock_templates_provider_clear_user_templates.assert_not_called()
