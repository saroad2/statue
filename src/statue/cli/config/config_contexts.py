"""Context configuration CLI."""
import sys

import click

from statue.cli.common_flags import config_path_option
from statue.cli.config.config_cli import config_cli
from statue.cli.config.interactive_adders.interactive_context_adder import (
    InteractiveContextAdder,
)
from statue.cli.styled_strings import failure_style, name_style
from statue.config.configuration import Configuration
from statue.exceptions import UnknownContext


@config_cli.command("add-context")
@config_path_option
def add_context_cli(config):
    """Add new context to configuration."""
    if config is None:
        config = Configuration.configuration_path()
    configuration = Configuration.from_file(config)
    InteractiveContextAdder.add_context(configuration.contexts_repository)
    configuration.to_toml(config)
    click.echo("Context was successfully added!")


@config_cli.command("edit-context")
@config_path_option
@click.argument("context_name", type=str)
def edit_context_cli(config, context_name):
    """Edit context from configuration."""
    if config is None:
        config = Configuration.configuration_path()
    configuration = Configuration.from_file(config)
    InteractiveContextAdder.edit_context(
        name=context_name, contexts_repository=configuration.contexts_repository
    )
    configuration.to_toml(config)
    click.echo(f"{name_style(context_name)} was successfully edited!")


@config_cli.command("remove-context")
@config_path_option
@click.argument("context_name", type=str)
def remove_context_cli(config, context_name):
    """Remove context from configuration."""
    if config is None:
        config = Configuration.configuration_path()
    configuration = Configuration.from_file(config)
    try:
        context = configuration.contexts_repository[context_name]
    except UnknownContext as error:
        click.echo(failure_style(str(error)))
        sys.exit(1)
    if not click.confirm(
        f"Are you sure you would like to remove the context {name_style(context_name)} "
        "and all of its references from configuration?",
    ):
        click.echo("Abort!")
        return
    configuration.remove_context(context)
    configuration.to_toml(config)
    click.echo(f"{name_style(context_name)} was successfully removed!")
