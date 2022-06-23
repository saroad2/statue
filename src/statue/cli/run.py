# pylint: disable=too-many-locals
"""Run CLI."""
from pathlib import Path
from typing import List, Optional, Sequence

import click

from statue.cli.cli import pass_configuration, statue_cli
from statue.cli.cli_util import list_or_none
from statue.cli.common_flags import (
    allow_option,
    contexts_option,
    deny_option,
    silent_option,
    verbose_option,
    verbosity_option,
)
from statue.cli.string_util import (
    boxed_string,
    evaluation_string,
    evaluation_summary_string,
)
from statue.cli.styled_strings import failure_style
from statue.commands_map_builder import CommandsMapBuilder
from statue.config.configuration import Configuration
from statue.exceptions import CommandsMapBuilderError, UnknownContext
from statue.runner import RunnerMode, build_runner
from statue.verbosity import is_silent, is_verbose


@statue_cli.command("run", short_help="Run static code analysis commands on sources.")
@click.argument("sources", type=click.Path(exists=True, path_type=Path), nargs=-1)
@contexts_option
@allow_option
@deny_option
@click.option(
    "-i", "--install", is_flag=True, help="Install commands before running if missing"
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
@click.option(
    "-f", "--failed", is_flag=True, help="Run commands from the most recent failed run"
)
@click.option(
    "-fo",
    "--failed-only",
    is_flag=True,
    help=(
        'Same as "--failed", but will only run the commands '
        "and not those who ended successfully"
    ),
)
@click.option(
    "--cache/--no-cache", default=True, help="Save evaluation to cache or not"
)
@silent_option
@verbose_option
@verbosity_option
@click.option(
    "--mode",
    type=click.Choice([mode.name.lower() for mode in RunnerMode], case_sensitive=False),
    callback=lambda ctx, param, value: (None if value is None else value.upper()),
    help="Should run asynchronously or not.",
)
@click.option(
    "-o",
    "--output",
    type=click.Path(dir_okay=False, path_type=Path),
    help="Output path to save evaluation result",
)
@click.pass_context
@pass_configuration
def run_cli(  # pylint: disable=too-many-arguments
    configuration: Configuration,
    ctx: click.Context,
    sources: Sequence[Path],
    context: Sequence[str],
    allow: Optional[List[str]],
    deny: Optional[List[str]],
    previous: Optional[int],
    failed: bool,
    failed_only: bool,
    install: bool,
    cache: bool,
    verbosity: str,
    mode: Optional[str],
    output: Optional[Path],
) -> None:
    """
    Run static code analysis commands on sources.

    Source files to run Statue on can be presented as positional arguments.
    When no source files are presented, will use configuration file to determine on
    which files to run
    """
    commands_map = None
    try:
        commands_map = CommandsMapBuilder(
            configuration=configuration,
            specified_sources=list_or_none(sources),
            allowed_commands=list_or_none(allow),
            denied_commands=list_or_none(deny),
            contexts=[
                configuration.contexts_repository[context_name]
                for context_name in context
            ],
            previous=previous,
            failed=failed,
            failed_only=failed_only,
        ).build()
    except (UnknownContext, CommandsMapBuilderError) as error:
        click.echo(failure_style(str(error)))
        ctx.exit(1)
    if len(commands_map) == 0:
        click.echo("No commands to run.")
        ctx.exit(0)
    missing_commands = [
        command_builder
        for command_builder in configuration.commands_repository
        if command_builder.name in commands_map.command_names
        and not command_builder.installed_correctly()
    ]
    __handle_missing_commands(
        ctx=ctx,
        missing_commands=missing_commands,
        install=install,
        verbosity=verbosity,
    )
    mode = mode if mode is not None else configuration.default_mode.name
    if is_verbose(verbosity):
        click.echo(f"Running evaluation in {mode.lower()} mode")
    runner = build_runner(mode)
    evaluation = runner.evaluate(commands_map)
    if not is_silent(verbosity):
        click.echo(boxed_string("Evaluation"))
        click.echo(evaluation_string(evaluation, verbosity=verbosity))
    if cache and configuration.cache.enabled:
        configuration.cache.save_evaluation(evaluation)
    if output is not None:
        evaluation.save_as_json(output)
    click.echo()
    if not is_silent(verbosity):
        click.echo(boxed_string("Summary"))
        click.echo()
    click.echo(evaluation_summary_string(evaluation))
    exit_code = 0 if evaluation.success else 1
    ctx.exit(exit_code)


def __handle_missing_commands(ctx, missing_commands, install, verbosity):
    if len(missing_commands) == 0:
        return
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
