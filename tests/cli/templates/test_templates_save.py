from statue.cli import statue_cli
from statue.exceptions import StatueTemplateError


def test_templates_save_without_override(
    cli_runner,
    mock_configuration_path,
    mock_build_configuration_from_file,
    mock_templates_provider_save_template,
):
    template_name = "name"

    result = cli_runner.invoke(statue_cli, ["templates", "save", template_name])

    assert result.exit_code == 0
    assert result.output == f'Template "{template_name}" was saved successfully!\n'
    mock_configuration_path.assert_called_once_with()
    mock_build_configuration_from_file.assert_called_once_with(
        mock_configuration_path.return_value
    )
    mock_templates_provider_save_template.assert_called_once_with(
        configuration=mock_build_configuration_from_file.return_value,
        name=template_name,
        override=False,
    )


def test_templates_save_with_override(
    cli_runner,
    mock_configuration_path,
    mock_build_configuration_from_file,
    mock_templates_provider_save_template,
):
    template_name = "name"

    result = cli_runner.invoke(
        statue_cli, ["templates", "save", template_name, "--override"]
    )

    assert result.exit_code == 0
    assert result.output == f'Template "{template_name}" was saved successfully!\n'
    mock_configuration_path.assert_called_once_with()
    mock_build_configuration_from_file.assert_called_once_with(
        mock_configuration_path.return_value
    )
    mock_templates_provider_save_template.assert_called_once_with(
        configuration=mock_build_configuration_from_file.return_value,
        name=template_name,
        override=True,
    )


def test_templates_save_with_configuration_file(
    cli_runner,
    tmp_path,
    mock_configuration_path,
    mock_build_configuration_from_file,
    mock_templates_provider_save_template,
):
    config_path = tmp_path / "statue.toml"
    config_path.touch()
    template_name = "name"

    result = cli_runner.invoke(
        statue_cli, ["templates", "save", template_name, "--config", str(config_path)]
    )

    assert result.exit_code == 0
    assert result.output == f'Template "{template_name}" was saved successfully!\n'
    mock_configuration_path.assert_not_called()
    mock_build_configuration_from_file.assert_called_once_with(config_path)
    mock_templates_provider_save_template.assert_called_once_with(
        configuration=mock_build_configuration_from_file.return_value,
        name=template_name,
        override=False,
    )


def test_templates_save_fail_due_to_template_error(
    cli_runner,
    mock_configuration_path,
    mock_build_configuration_from_file,
    mock_templates_provider_save_template,
):
    error_content = "This is an error"
    template_name = "name"

    mock_templates_provider_save_template.side_effect = StatueTemplateError(
        error_content
    )
    result = cli_runner.invoke(statue_cli, ["templates", "save", template_name])

    assert result.exit_code == 1
    assert result.output == f"{error_content}\n"
    mock_configuration_path.assert_called_once_with()
    mock_build_configuration_from_file.assert_called_once_with(
        mock_configuration_path.return_value
    )
    mock_templates_provider_save_template.assert_called_once_with(
        configuration=mock_build_configuration_from_file.return_value,
        name=template_name,
        override=False,
    )
