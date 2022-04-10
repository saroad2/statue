"""Utility module for interactive adders."""
import click

from statue.cli.styled_strings import failure_style, name_style


def get_help_string(name: str) -> str:
    """
    Get help string for an object.

    :param name: Name of the object to get help for
    :type name: str
    :return: help string for the object
    :rtype: str
    """
    help_string = ""
    while help_string == "":
        help_string = click.prompt(
            f"Please add help string for {name_style(name)}",
            default="",
            show_default=False,
        )
        help_string = help_string.strip()
        if help_string == "":
            click.echo(failure_style("Help string cannot be empty!"))
    return help_string
