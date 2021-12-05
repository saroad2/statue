# pylint: disable=too-many-locals
"""Run CLI."""
from itertools import chain
from pathlib import Path
from typing import List, Optional, Union

import click

from statue.cache import Cache
from statue.cli.cli import statue_cli
from statue.cli.util import (
    allow_option,
    contexts_option,
    deny_option,
    failure_style,
    silent_option,
    verbose_option,
    verbosity_option,
)
from statue.commands_map import read_commands_map
from statue.evaluation import Evaluation, evaluate_commands_map
from statue.exceptions import MissingConfiguration, UnknownContext
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
@click.option(
    "-f",
    "--failed",
    is_flag=True,
    help=(
        "Run failed commands of an earlier evaluation. "
        "Run over the most recent evaluation by default"
    ),
)
@click.option(
    "-p",
    "--previous",
    type=int,
    help=(
        "Run commands of the nth recent evaluation. "
        'combine this flag with "-f" in order to run only failed commands from that '
        "evaluation"
    ),
)
@click.option(
    "-r",
    "--recent",
    "previous",
    flag_value=1,
    type=int,
    help='Run commands of the most recent evaluation. Same as "--previous 1".',
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
    previous: Optional[int],
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
            sources=sources,
            context=context,
            allow=allow,
            deny=deny,
            failed=failed,
            previous=previous,
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

    missing_commands = [
        command
        for command in chain.from_iterable(commands_map.values())
        if not command.installed_correctly()
    ]
    if len(missing_commands) != 0:
        if install:
            for command in missing_commands:
                command.update_to_version(verbosity=verbosity)
        else:
            missing_commands_names = [command.name for command in missing_commands]
            click.echo(
                failure_style(
                    "The following commands are not installed correctly: "
                    f"{', '.join(missing_commands_names)}"
                )
            )
            click.echo(
                "Consider using the '-i' flag in order to install missing "
                "commands before running"
            )
            ctx.exit(1)
    if not is_silent(verbosity):
        print_boxed("Evaluation", print_method=click.echo)
    evaluation = evaluate_commands_map(
        commands_map=commands_map, verbosity=verbosity, print_method=click.echo
    )
    if cache:
        Cache.save_evaluation(evaluation)
    if output is not None:
        evaluation.save_as_json(output)
    click.echo()
    if not is_silent(verbosity):
        print_boxed("Summary", print_method=click.echo)
        click.echo()
    ctx.exit(__evaluate_failure_map(evaluation.failure_map))


def __evaluate_failure_map(failure_map):
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
    sources, context, allow, deny, failed, previous
):
    if failed and previous is None:
        previous = 1
    if previous is None:
        return read_commands_map(
            sources,
            contexts=context,
            allow_list=allow,
            deny_list=deny,
        )
    evaluation_path = Cache.evaluation_path(previous - 1)
    if evaluation_path is None or not evaluation_path.exists():
        return None
    evaluation = Evaluation.load_from_file(evaluation_path)
    if failed:
        return evaluation.failure_map
    return evaluation.commands_map
