"""Run CLI."""
from itertools import chain
from pathlib import Path
from typing import List, Optional, Union

import click

from statue.cache import Cache
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
from statue.commands_map import read_commands_map
from statue.evaluation import Evaluation, evaluate_commands_map, get_failure_map
from statue.exceptions import (
    CommandExecutionError,
    MissingConfiguration,
    UnknownContext,
)
from statue.print_util import print_boxed
from statue.verbosity import is_silent


@statue_cli.command("run")
@click.pass_context
@click.argument("sources", nargs=-1)
@contexts_option
@allow_option
@deny_option
@click.option(
    "-i", "--install", is_flag=True, help="Install commands before running if missing"
)
@click.option("-f", "--failed", is_flag=True, help="Run failed commands")
@click.option(
    "--cache/--no-cache", default=True, help="Save evaluation to cache or not"
)
@silent_option
@verbose_option
@verbosity_option
@click.option(
    "-o",
    "--output",
    type=click.Path(dir_okay=False),
    help="Output path to save evaluation result",
)
def run_cli(  # pylint: disable=too-many-arguments
    ctx: click.Context,
    sources: List[Union[Path, str]],
    context: Optional[List[str]],
    allow: Optional[List[str]],
    deny: Optional[List[str]],
    failed: bool,
    install: bool,
    cache: bool,
    verbosity: str,
    output: Optional[str],
) -> None:
    """
    Run static code analysis commands on sources.

    Source files to run Statue on can be presented as positional arguments.
    When no source files are presented, will use configuration file to determine on
    which files to run
    """
    commands_map = None
    try:
        commands_map = __get_commands_map(
            sources=sources, context=context, allow=allow, deny=deny, failed=failed
        )
    except UnknownContext as error:
        click.echo(error)
        ctx.exit(1)
    except MissingConfiguration:
        click.echo(
            '"Run" command cannot be run without a specified source '
            "or a sources section in Statue's configuration."
        )
        click.echo(
            'Please consider running "statue config init" in order to initialize '
            "default configuration."
        )
        ctx.exit(1)
    if commands_map is None or len(commands_map) == 0:
        click.echo(ctx.get_help())
        return

    if install:
        install_commands_if_missing(
            list(chain.from_iterable(commands_map.values())), verbosity=verbosity
        )
    if not is_silent(verbosity):
        print_boxed("Evaluation", print_method=click.echo)
    evaluation = None
    try:
        evaluation = evaluate_commands_map(
            commands_map=commands_map, verbosity=verbosity, print_method=click.echo
        )
    except CommandExecutionError as error:
        click.echo(str(error))
        click.echo('Try to rerun with the "-i" flag')
        ctx.exit(1)
    if cache:
        evaluation.save_as_json(Cache.last_evaluation_path())
    if output is not None:
        evaluation.save_as_json(output)
    click.echo()
    if not is_silent(verbosity):
        print_boxed("Summary", print_method=click.echo)
        click.echo()
    failure_map = get_failure_map(evaluation)
    ctx.exit(__evaluate_failure_map(failure_map))


def __evaluate_failure_map(failure_map):
    """Returns exit code."""
    if len(failure_map) == 0:
        click.echo("Statue finished successfully!")
        return 0
    click.echo("Statue has failed on the following commands:")
    click.echo()
    for input_path, failed_commands in failure_map.items():
        click.echo(f"{input_path}:")
        click.echo(f"\t{', '.join([command.name for command in failed_commands])}")
    return 1


def __get_commands_map(  # pylint: disable=too-many-arguments
    sources, context, allow, deny, failed
):
    commands_map = None
    if failed and Cache.last_evaluation_path().exists():
        commands_map = get_failure_map(
            Evaluation.load_from_file(Cache.last_evaluation_path())
        )
    if commands_map is None or len(commands_map) == 0:
        commands_map = read_commands_map(
            sources,
            contexts=context,
            allow_list=allow,
            deny_list=deny,
        )
    return commands_map
