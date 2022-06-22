"""Commands CLI."""
import click

from statue.cli.cli import pass_configuration, statue_cli
from statue.cli.common_flags import silent_option, verbose_option, verbosity_option
from statue.cli.styled_strings import bullet_style, name_style
from statue.config.configuration import Configuration
from statue.exceptions import UnknownCommand


@statue_cli.group("commands")
def commands_cli() -> None:
    """Commands related actions such as list, install, show, etc."""


@commands_cli.command("list")
@pass_configuration
def list_commands_cli(configuration: Configuration) -> None:
    """List matching commands to contexts, allow list and deny list."""
    for command_builder in configuration.commands_repository:
        name = name_style(command_builder.name)
        if command_builder.version is not None:
            name += f" (version: {command_builder.version})"
        click.echo(f"{name} - {command_builder.help}")


@commands_cli.command("install")
@silent_option
@verbose_option
@verbosity_option
@pass_configuration
def install_commands_cli(
    configuration: Configuration,
    verbosity: str,
) -> None:
    """Install missing commands."""
    for command_builder in configuration.commands_repository:
        if not command_builder.installed_correctly():
            command_builder.install(verbosity=verbosity)


@commands_cli.command("show")
@click.argument("command_name", type=str)
@click.pass_context
@pass_configuration
def show_command_cli(
    configuration: Configuration,
    ctx: click.Context,
    command_name: str,
) -> None:
    """Show information about specific command."""
    command_builder = None
    try:
        command_builder = configuration.commands_repository[command_name]
    except UnknownCommand as error:
        click.echo(str(error))
        ctx.exit(1)
    click.echo(f"{bullet_style('Name')} - {name_style(command_builder.name)}")
    if command_builder.version is not None:
        click.echo(f"{bullet_style('Version')} - {command_builder.version}")
    click.echo(f"{bullet_style('Description')} - {command_builder.help}")
    if len(command_builder.default_args) != 0:
        click.echo(
            f"{bullet_style('Default arguments')} - "
            f"{' '.join(command_builder.default_args)}"
        )
    if len(command_builder.required_contexts) != 0:
        required_contexts = [
            name_style(context.name) for context in command_builder.required_contexts
        ]
        required_contexts.sort()
        click.echo(
            f"{bullet_style('Required contexts')} - " f"{', '.join(required_contexts)}"
        )
    if len(command_builder.allowed_contexts) != 0:
        allowed_contexts = [
            name_style(context.name) for context in command_builder.allowed_contexts
        ]
        allowed_contexts.sort()
        click.echo(
            f"{bullet_style('Allowed contexts')} - " f"{', '.join(allowed_contexts)}"
        )
    if len(command_builder.denied_contexts) != 0:
        denied_contexts = [
            name_style(context.name) for context in command_builder.denied_contexts
        ]
        denied_contexts.sort()
        click.echo(
            f"{bullet_style('Denied contexts')} - " f"{', '.join(denied_contexts)}"
        )
    if len(command_builder.specified_contexts) == 0:
        return
    click.echo(f"{bullet_style('Specified contexts')}:")
    for (
        context,
        context_specification,
    ) in command_builder.contexts_specifications.items():
        click.echo(f"\t{name_style(context.name)}")
        if context_specification.args is not None:
            click.echo(
                f"\t\t{bullet_style('Override arguments')}: "
                f"{' '.join(context_specification.args)}"
            )
        if context_specification.add_args is not None:
            click.echo(
                f"\t\t{bullet_style('Added arguments')}: "
                f"{' '.join(context_specification.add_args)}"
            )
        if context_specification.clear_args:
            click.echo(f"\t\t{bullet_style('Clears arguments')}")
