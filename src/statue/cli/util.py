"""Utility methods for CLI."""
import click

from statue.verbosity import DEFAULT_VERBOSITY, SILENT, VERBOSE, VERBOSITIES

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


def name_style(name):
    """
    Styling function to emphasise names.

    :param name: The name to style
    :return: Styled name
    :rtype: str
    """
    return click.style(name, fg="magenta")


def bullet_style(bullet_name):
    """
    Styling function to emphasise bullet names.

    :param bullet_name: The name to style
    :return: Styled bullet name
    :rtype: str
    """
    return click.style(bullet_name, fg="yellow")


def success_style(success_string):
    """
    Styling function to emphasise bullet names.

    :param success_string: The string to style
    :return: Styled success string
    :rtype: str
    """
    return click.style(success_string, fg="green")


def failure_style(failure_string):
    """
    Styling function to emphasise bullet names.

    :param failure_string: The string to style
    :return: Styled failure string
    :rtype: str
    """
    return click.style(failure_string, fg="red")
