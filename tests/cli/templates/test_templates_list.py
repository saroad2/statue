from pytest_cases import THIS_MODULE, parametrize_with_cases

from statue.cli import statue_cli


def case_only_default_templates():
    default_templates = ["a", "b", "c"]
    user_templates = []
    output = "Default templates:\n\ta\n\tb\n\tc\nNo user templates.\n"
    return default_templates, user_templates, output


def case_only_default_and_user_templates():
    default_templates = ["a", "b", "c"]
    user_templates = ["d", "e", "f"]
    output = (
        "Default templates:\n"
        "\ta\n"
        "\tb\n"
        "\tc\n"
        "User templates:\n"
        "\td\n"
        "\te\n"
        "\tf\n"
    )
    return default_templates, user_templates, output


@parametrize_with_cases(
    argnames=["default_templates", "user_templates", "output"], cases=THIS_MODULE
)
def test_templates_list_cli(
    cli_runner,
    mock_templates_provider_default_names,
    mock_templates_provider_user_names,
    default_templates,
    user_templates,
    output,
):
    mock_templates_provider_default_names.return_value = default_templates
    mock_templates_provider_user_names.return_value = user_templates
    result = cli_runner.invoke(statue_cli, ["templates", "list"])

    assert result.exit_code == 0
    assert result.output == output
