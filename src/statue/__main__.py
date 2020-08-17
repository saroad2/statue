"""Main of Statue."""
import sys
from pathlib import Path
from typing import List, Optional, MutableMapping, Any, Union

import click

from statue import __version__
from statue.commands_map import get_commands_map
from statue.configuration import get_configuration
from statue.constants import COMMANDS
from statue.commands_reader import read_commands

from statue.verbosity import VERBOSITIES, DEFAULT_VERBOSITY, SILENT, VERBOSE, is_silent


def print_title(title: str, underline: str = "=") -> None:
    """
    Print a title with a title line under it.

    :param underline: Character to use as underline to the title
    :param title: The title to print
    """
    print(title.title())
    print(underline * len(title))


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


@click.group(invoke_without_command=True)
@click.pass_context
@click.version_option(version=__version__)
@click.option(
    "--config",
    envvar="STATUE_CONFIG",
    default=lambda: Path.cwd() / "statue.toml",
    type=click.Path(exists=True, dir_okay=False),
    help="Statue configuration file.",
)
def statue(
    ctx: click.Context, config: str,
):
    """Statue is a static code analysis tools orchestrator."""
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())
    ctx.obj = get_configuration(Path(config))


@statue.command("list")
@click.pass_obj
@contexts_option
@allow_option
@deny_option
def list_commands(
    statue_configuration: MutableMapping[str, Any],
    context: Optional[List[str]],
    allow: Optional[List[str]],
    deny: Optional[List[str]],
):
    """List matching commands to contexts, allow list and deny list."""
    commands = read_commands(
        statue_configuration[COMMANDS],
        contexts=context,
        allow_list=allow,
        deny_list=deny,
    )
    for command in commands:
        print(command.name, "-", command.help)


@statue.command()
@click.pass_context
@click.argument("sources", nargs=-1)
@contexts_option
@allow_option
@deny_option
@click.option(
    "--verbosity",
    type=click.Choice(VERBOSITIES, case_sensitive=False),
    default=DEFAULT_VERBOSITY,
    show_default=True,
)
@click.option(
    "--silent", "verbosity", flag_value=SILENT, help=f'Set verbosity to "{SILENT}".'
)
@click.option(
    "--verbose", "verbosity", flag_value=VERBOSE, help=f'Set verbosity to "{VERBOSE}".'
)
def run(
    ctx: click.Context,
    sources: List[Union[Path, str]],
    context: Optional[List[str]],
    allow: Optional[List[str]],
    deny: Optional[List[str]],
    verbosity: str,
):
    """
    Run static code analysis commands on sources.

    Source files to run Statue on can be presented as positional arguments.
    When no source files are presented, will use configuration file to determine on
    which files to run
    """
    statue_configuration = ctx.obj
    commands_map = get_commands_map(
        sources,
        statue_configuration,
        contexts=context,
        allow_list=allow,
        deny_list=deny,
    )
    if commands_map is None:
        click.echo(ctx.get_help())
        return

    failed_paths = dict()
    print_title("Evaluation")
    for input_path, commands in commands_map.items():
        if not is_silent(verbosity):
            print()
            print(f"Evaluating {input_path}")
        failed_commands = []
        for command in commands:
            if not is_silent(verbosity):
                print_title(command.name, underline="-")
            return_code = command.execute(input_path, verbosity)
            if return_code != 0:
                failed_commands.append(command.name)
        if len(failed_commands) != 0:
            failed_paths[input_path] = failed_commands
    print()
    print_title("Summary")
    if len(failed_paths) != 0:
        print("Statue has failed on the following commands:")
        print()
        for input_path, failed_commands in failed_paths.items():
            print(f"{input_path}:")
            print(f"\t{', '.join(failed_commands)}")
        sys.exit(1)
    else:
        print("Statue finished successfully!")


if __name__ == "__main__":
    statue()
