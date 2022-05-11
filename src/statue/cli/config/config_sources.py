"""Sources configuration CLI."""
import sys
from pathlib import Path
from typing import List, Optional

import click

from statue.cli.common_flags import config_path_option
from statue.cli.config.config_cli import config_cli
from statue.cli.config.interactive_adders.interactive_sources_adder import (
    InteractiveSourcesAdder,
)
from statue.cli.styled_strings import failure_style, source_style
from statue.config.configuration import Configuration


@config_cli.command("add-source")
@click.argument("sources", type=click.Path(exists=True, path_type=Path), nargs=-1)
@config_path_option
def add_source_to_configuration_cli(config: Optional[Path], sources: List[Path]):
    """Add new source to configuration."""
    if config is None:
        config = Configuration.configuration_path()
    configuration = Configuration.from_file(config)
    InteractiveSourcesAdder.update_sources_repository(configuration, list(sources))
    configuration.to_toml(config)
    click.echo("Sources were added successfully!")


@config_cli.command("edit-source")
@click.argument("source", type=click.Path(exists=True, path_type=Path))
@config_path_option
def edit_source_in_configuration_cli(config: Optional[Path], source: Path):
    """Edit a source from configuration."""
    if config is None:
        config = Configuration.configuration_path()
    configuration = Configuration.from_file(config)
    if source not in configuration.sources_repository.sources_list:
        click.echo(failure_style(f"{source} is not specified in configuration"))
        sys.exit(1)
    configuration.sources_repository[source] = InteractiveSourcesAdder.get_filter(
        configuration=configuration, source=source
    )


@config_cli.command("remove-source")
@click.argument("source", type=click.Path(exists=True, path_type=Path))
@config_path_option
def remove_source_from_configuration_cli(config: Optional[Path], source: Path):
    """Remove context from configuration."""
    if config is None:
        config = Configuration.configuration_path()
    configuration = Configuration.from_file(config)
    if source not in configuration.sources_repository.sources_list:
        click.echo(failure_style(f"Could not find {source} in configuration."))
        sys.exit(1)
    if not click.confirm(
        f"Are you sure you would like to remove the source {source_style(str(source))} "
        "from configuration?",
    ):
        click.echo("Abort!")
        return
    configuration.sources_repository.remove_source(source)
    configuration.to_toml(config)
    click.echo(f"{source_style(str(source))} was successfully removed!")
