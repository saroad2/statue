"""Contexts CLI."""
from typing import Any, MutableMapping

import click

from statue.cli.cli import statue as statue_cli
from statue.constants import CONTEXTS, HELP


@statue_cli.command()
@click.pass_obj
def contexts(statue_configuration: MutableMapping[str, Any]) -> None:
    """Print all available contexts."""
    for context_name, context in statue_configuration[CONTEXTS].items():
        click.echo(f"{context_name} - {context[HELP]}")
