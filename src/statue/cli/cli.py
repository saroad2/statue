"""Main CLI for statue."""
from pathlib import Path

import click

from statue import __version__
from statue.configuration import Configuration


@click.group(invoke_without_command=True)
@click.pass_context
@click.version_option(version=__version__)
@click.option(
    "--config",
    envvar="STATUE_CONFIG",
    default=lambda: str(Path.cwd() / "statue.toml"),
    type=click.Path(exists=True, dir_okay=False),
    help="Statue configuration file.",
)
def statue(
    ctx: click.Context,
    config: str,
) -> None:
    """Statue is a static code analysis tools orchestrator."""
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())
    Configuration.load_configuration(Path(config))
