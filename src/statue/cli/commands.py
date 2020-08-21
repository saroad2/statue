"""Commands CLI."""
from typing import Any, List, MutableMapping, Optional

import click

from statue.cli.cli import statue as statue_cli
from statue.cli.util import (
    allow_option,
    contexts_option,
    deny_option,
    install_commands_if_missing,
    silent_option,
    verbose_option,
    verbosity_option,
)
from statue.commands_reader import read_commands
from statue.constants import COMMANDS


@statue_cli.command("list")
@click.pass_obj
@contexts_option
@allow_option
@deny_option
def list_commands(
    statue_configuration: MutableMapping[str, Any],
    context: Optional[List[str]],
    allow: Optional[List[str]],
    deny: Optional[List[str]],
) -> None:
    """List matching commands to contexts, allow list and deny list."""
    commands = read_commands(
        statue_configuration[COMMANDS],
        contexts=context,
        allow_list=allow,
        deny_list=deny,
    )
    for command in commands:
        print(command.name, "-", command.help)


@statue_cli.command("install")
@click.pass_obj
@contexts_option
@allow_option
@deny_option
@verbosity_option
@silent_option
@verbose_option
def install_commands(
    statue_configuration: MutableMapping[str, Any],
    context: Optional[List[str]],
    allow: Optional[List[str]],
    deny: Optional[List[str]],
    verbosity: str,
) -> None:
    """Install missing commands."""
    install_commands_if_missing(
        read_commands(
            statue_configuration[COMMANDS],
            contexts=context,
            allow_list=allow,
            deny_list=deny,
        ),
        verbosity=verbosity,
    )
