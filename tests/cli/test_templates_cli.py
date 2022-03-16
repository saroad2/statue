from statue.cli import statue_cli
from statue.constants import ENCODING
from statue.exceptions import UnknownTemplate


def test_templates_list(cli_runner, mock_templates_provider_names):
    name1, name2, name3 = "a", "b", "c"
    mock_templates_provider_names.return_value = [name1, name2, name3]

    result = cli_runner.invoke(statue_cli, ["templates", "list"])

    assert result.exit_code == 0
    assert result.output == "a\nb\nc\n"


def test_template_show_successful(
    cli_runner, mock_templates_provider_get_template_path, tmp_path
):
    template_name = "my template"
    template_path = tmp_path / "my_template.txt"
    line1, line2, line3 = (
        "this is a line\n",
        "this is also a line\n",
        "too many lines!\n",
    )
    with open(template_path, mode="w", encoding=ENCODING) as template_file:
        template_file.writelines([line1, line2, line3])
    mock_templates_provider_get_template_path.return_value = template_path

    result = cli_runner.invoke(statue_cli, ["templates", "show", template_name])
    assert result.exit_code == 0
    assert result.output == f"{line1}{line2}{line3}\n"


def test_template_show_failure(
    cli_runner,
    mock_templates_provider_get_template_path,
):
    template_name = "my template"
    mock_templates_provider_get_template_path.side_effect = UnknownTemplate(
        template_name
    )

    result = cli_runner.invoke(statue_cli, ["templates", "show", template_name])
    assert result.exit_code == 1
    assert result.output == f'Could not find template named "{template_name}"\n'
