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
from statue.commands_map import get_commands_map
from statue.evaluation import evaluate_commands_map, get_failure_map
from statue.excptions import UnknownContext
from statue.print_util import print_title


@statue_cli.command("run")
@click.pass_context
@click.argument("sources", nargs=-1)
@contexts_option
@allow_option
@deny_option
@click.option(
    "-i",
    "--install",
    is_flag=True,
    help="Install commands before running if missing",
)
@silent_option
@verbose_option  # pylint: disable=R0913
@verbosity_option
def run_cli(  # pylint: disable=too-many-arguments
    ctx: click.Context,
    sources: List[Union[Path, str]],
    context: Optional[List[str]],
    allow: Optional[List[str]],
    deny: Optional[List[str]],
    install: bool,
    verbosity: str,
) -> None:
    """
    Run static code analysis commands on sources.

    Source files to run Statue on can be presented as positional arguments.
    When no source files are presented, will use configuration file to determine on
    which files to run
    """
    try:
        commands_map = get_commands_map(
            sources,
            contexts=context,
            allow_list=allow,
            deny_list=deny,
        )
    except UnknownContext as error:
        click.echo(error)
        ctx.exit(1)
    if commands_map is None or len(commands_map) == 0:
        click.echo(ctx.get_help())
        return

    if install:
        install_commands_if_missing(
            list(chain.from_iterable(commands_map.values())), verbosity=verbosity
        )
    print_title("Evaluation")
    evaluation = evaluate_commands_map(
        commands_map=commands_map, verbosity=verbosity, print_method=click.echo
    )
    evaluation.save_as_json(Cache.cache_file("evaluation.json"))
    click.echo()
    print_title("Summary")
    failed_paths = get_failure_map(evaluation)
    if len(failed_paths) != 0:
        click.echo("Statue has failed on the following commands:")
        click.echo()
        for input_path, failed_commands in failed_paths.items():
            click.echo(f"{input_path}:")
            click.echo(f"\t{', '.join(failed_commands)}")
        ctx.exit(1)
    else:
        click.echo("Statue finished successfully!")
