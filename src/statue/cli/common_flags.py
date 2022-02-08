"""Common flags used by multiple CLIs."""
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
