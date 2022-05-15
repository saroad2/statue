from statue.cli import statue_cli
from statue.constants import ENCODING
from statue.exceptions import UnknownTemplate


def test_template_show_print_lines(
    cli_runner, tmp_path, mock_templates_provider_get_template_path
):
    template_name = "name"
    template_path = tmp_path / "template.toml"
    content = [
        "This is a line\n",
        "This is also a line\n",
        "That's something new\n",
    ]
    with open(template_path, mode="w", encoding=ENCODING) as template_file:
        template_file.writelines(content)

    mock_templates_provider_get_template_path.return_value = template_path

    result = cli_runner.invoke(statue_cli, ["templates", "show", template_name])

    assert result.exit_code == 0
    assert result.output == "".join(content) + "\n"


def test_template_show_raises_unknown_template(
    cli_runner, mock_templates_provider_get_template_path
):
    template_name = "name"

    mock_templates_provider_get_template_path.side_effect = UnknownTemplate(
        template_name
    )

    result = cli_runner.invoke(statue_cli, ["templates", "show", template_name])

    assert result.exit_code == 1
    assert result.output == f'Could not find template named "{template_name}"\n'
