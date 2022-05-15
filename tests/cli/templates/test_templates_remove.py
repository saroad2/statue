import pytest

from statue.cli import statue_cli


def test_templates_simple_remove(
    cli_runner,
    mock_templates_provider_default_names,
    mock_templates_provider_user_names,
    mock_templates_provider_remove_template,
):
    template_name = "name"

    mock_templates_provider_default_names.return_value = []
    mock_templates_provider_user_names.return_value = [template_name]
    result = cli_runner.invoke(
        statue_cli, ["templates", "remove", template_name], input="y\n"
    )

    assert result.exit_code == 0
    assert result.output == (
        'Are you sure you want to remove template "name"? [y/N]: y\n'
        f'Template "{template_name}" was saved successfully!\n'
    )
    mock_templates_provider_remove_template.assert_called_once_with(template_name)


def test_templates_remove_fail_due_to_default_template(
    cli_runner,
    mock_templates_provider_default_names,
    mock_templates_provider_user_names,
    mock_templates_provider_remove_template,
):
    template_name = "name"

    mock_templates_provider_default_names.return_value = [template_name]
    mock_templates_provider_user_names.return_value = []
    result = cli_runner.invoke(statue_cli, ["templates", "remove", template_name])

    assert result.exit_code == 1
    assert result.output == "Cannot remove a default template.\n"
    mock_templates_provider_remove_template.assert_not_called()


def test_templates_remove_fail_due_to_non_existing_template(
    cli_runner,
    mock_templates_provider_default_names,
    mock_templates_provider_user_names,
    mock_templates_provider_remove_template,
):
    template_name = "name"

    mock_templates_provider_default_names.return_value = []
    mock_templates_provider_user_names.return_value = []
    result = cli_runner.invoke(statue_cli, ["templates", "remove", template_name])

    assert result.exit_code == 1
    assert result.output == f'Could not find template named "{template_name}"\n'
    mock_templates_provider_remove_template.assert_not_called()


@pytest.mark.parametrize("confirm_response", ["", "n", "N"])
def test_templates_remove_fail_due_to_no_confirmation(
    cli_runner,
    confirm_response,
    mock_templates_provider_default_names,
    mock_templates_provider_user_names,
    mock_templates_provider_remove_template,
):
    template_name = "name"

    mock_templates_provider_default_names.return_value = []
    mock_templates_provider_user_names.return_value = [template_name]
    result = cli_runner.invoke(
        statue_cli,
        ["templates", "remove", template_name],
        input=f"{confirm_response}\n",
    )

    assert result.exit_code == 1
    assert result.output == (
        f'Are you sure you want to remove template "{template_name}"? [y/N]: '
        f"{confirm_response}\nAbort!\n"
    )
    mock_templates_provider_remove_template.assert_not_called()
