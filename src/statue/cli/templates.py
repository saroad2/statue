"""Templates CLI."""
import sys

import click

from statue.cli.cli import statue_cli
from statue.cli.common_flags import config_path_option
from statue.cli.styled_strings import bullet_style, failure_style, name_style
from statue.config.configuration import Configuration
from statue.exceptions import StatueTemplateError, UnknownTemplate
from statue.templates.templates_provider import TemplatesProvider


@statue_cli.group("templates")
def templates_cli() -> None:
    """Template related actions such as list, show, etc."""


@templates_cli.command("list")
def list_templates_cli():
    """List all available templates."""
    click.echo(bullet_style("Default templates:"))
    for template_name in TemplatesProvider.default_templates_names():
        click.echo(f"\t{name_style(template_name)}")
    user_templates = TemplatesProvider.user_templates_names()
    if len(user_templates) == 0:
        click.echo("No user templates.")
        return
    click.echo(bullet_style("User templates:"))
    for template_name in user_templates:
        click.echo(f"\t{name_style(template_name)}")


@templates_cli.command("show")
@click.argument("template_name", type=str)
def show_templates_cli(template_name):
    """Show template by name."""
    try:
        template_path = TemplatesProvider.get_template_path(template_name)
    except UnknownTemplate as error:
        click.echo(failure_style(str(error)))
        sys.exit(1)
    with template_path.open(mode="r") as template_file:
        template_lines = template_file.readlines()
    click.echo("".join(template_lines))


@templates_cli.command("save")
@click.argument("template_name", type=str)
@config_path_option
@click.option(
    "--override/-no-override",
    is_flag=True,
    default=False,
    help="Override template with given name if already exists.",
)
def save_templates_cli(template_name, config, override):
    """Save current configuration as template."""
    if config is None:
        config = Configuration.configuration_path()
    configuration = Configuration.from_file(config)
    configuration.sources_repository.reset()
    try:
        TemplatesProvider.save_template(
            name=template_name, configuration=configuration, override=override
        )
    except StatueTemplateError as error:
        click.echo(failure_style(str(error)))
        sys.exit(1)
    click.echo(f'Template "{template_name}" was saved successfully!')


@templates_cli.command("remove")
@click.argument("template_name", type=str)
def remove_templates_cli(template_name):
    """Remove template by name."""
    if template_name in TemplatesProvider.default_templates_names():
        click.echo(failure_style("Cannot remove a default template."))
        sys.exit(1)
    if template_name not in TemplatesProvider.user_templates_names():
        click.echo(failure_style(f'Could not find template named "{template_name}"'))
        sys.exit(1)
    if not click.confirm(
        f'Are you sure you want to remove template "{template_name}"?', default=False
    ):
        click.echo(failure_style("Abort!"))
        sys.exit(1)
    TemplatesProvider.remove_template(template_name)
    click.echo(f'Template "{template_name}" was saved successfully!')


@templates_cli.command("clear")
def clear_user_templates_cli():
    """Remove template by name."""
    templates_number = len(TemplatesProvider.user_templates_names())
    if templates_number == 0:
        click.echo("No templates to remove.")
        return
    if not click.confirm(
        f"Are you sure you want to remove {templates_number} templates?", default=False
    ):
        click.echo(failure_style("Abort!"))
        sys.exit(1)
    TemplatesProvider.clear_user_templates()
    click.echo("All user templates were successfully remove!")
