"""Utility methods for CLI."""
from typing import List

import click

from statue.command import Command
from statue.verbosity import DEFAULT_VERBOSITY, SILENT, VERBOSE, VERBOSITIES


def print_title(title: str, underline: str = "=") -> None:
    """
    Print a title with a title line under it.

    :param underline: Character to use as underline to the title
    :param title: The title to print
    """
    print(title.title())
    print(underline * len(title))


def install_commands_if_missing(
    commands_list: List[Command], verbosity: str = DEFAULT_VERBOSITY
) -> None:
    """
    Install commands if missing using `pip install`.

    :param commands_list: list of :class:`Command` items
    :param verbosity: String. Verbosity level
    """
    uninstalled_commands = [
        command for command in commands_list if not command.installed()
    ]
    if len(uninstalled_commands) == 0:
        print("All commands are installed!")
    else:
        installed = []
        print(
            "The following commands are not installed: "
            f"{', '.join([command.name for command in uninstalled_commands])}"
        )
        for command in uninstalled_commands:
            if command.name in installed:
                continue
            command.install(verbosity)
            installed.append(command.name)


contexts_option = click.option(
    "-c",
    "--context",
    type=str,
    default=None,
    multiple=True,
    help="Context in which to evaluate the commands.",
)
allow_option = click.option(
    "-a", "--allow", type=str, default=None, multiple=True, help="Allowed command."
)
deny_option = click.option(
    "-d", "--deny", type=str, default=None, multiple=True, help="Denied command."
)
verbosity_option = click.option(
    "--verbosity",
    type=click.Choice(VERBOSITIES, case_sensitive=False),
    default=DEFAULT_VERBOSITY,
    show_default=True,
)

silent_option = click.option(
    "--silent", "verbosity", flag_value=SILENT, help=f'Set verbosity to "{SILENT}".'
)

verbose_option = click.option(
    "--verbose", "verbosity", flag_value=VERBOSE, help=f'Set verbosity to "{VERBOSE}".'
)
