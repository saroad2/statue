"""Context configuration CLI."""
import click

from statue.cli.common_flags import config_path_option
from statue.cli.config.config_cli import config_cli
from statue.cli.config.interactive_adders.interactive_context_adder import (
    InteractiveContextAdder,
)
from statue.cli.styled_strings import name_style
from statue.config.configuration_builder import ConfigurationBuilder


@config_cli.command("add-context")
@config_path_option
def add_context_cli(config):
    """Add new context to configuration."""
    if config is None:
        config = ConfigurationBuilder.configuration_path()
    configuration = ConfigurationBuilder.build_configuration_from_file(config)
    InteractiveContextAdder.add_context(configuration.contexts_repository)
    configuration.to_toml(config)
    click.echo("Context was successfully added!")


@config_cli.command("edit-context")
@config_path_option
@click.argument("context_name", type=str)
def edit_context_cli(config, context_name):
    """Edit context from configuration."""
    if config is None:
        config = ConfigurationBuilder.configuration_path()
    configuration = ConfigurationBuilder.build_configuration_from_file(config)
    InteractiveContextAdder.edit_context(
        name=context_name, contexts_repository=configuration.contexts_repository
    )
    configuration.to_toml(config)
    click.echo(f"{name_style(context_name)} was successfully edited!")
