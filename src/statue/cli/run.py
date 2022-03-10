# pylint: disable=too-many-locals
"""Run CLI."""
from pathlib import Path
from typing import List, Optional, Sequence, Union

import click

from statue.cli.cli import pass_configuration, statue_cli
from statue.cli.common_flags import (
    allow_option,
    contexts_option,
    deny_option,
    silent_option,
    verbose_option,
    verbosity_option,
)
from statue.cli.string_util import boxed_string, evaluation_string
from statue.cli.styled_strings import (
    failure_style,
    name_style,
    source_style,
    success_style,
)
from statue.commands_filter import CommandsFilter
from statue.config.configuration import Configuration
from statue.evaluation import Evaluation
from statue.exceptions import UnknownContext
from statue.runner import RunnerMode, build_runner
from statue.verbosity import is_silent, is_verbose


@statue_cli.command("run")
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
    "--mode",
    type=click.Choice([mode.name.lower() for mode in RunnerMode], case_sensitive=False),
    callback=lambda ctx, param, value: (None if value is None else value.upper()),
    help="Should run asynchronously or not.",
)
@click.option(
    "-o",
    "--output",
    type=click.Path(dir_okay=False),
    help="Output path to save evaluation result",
)
@click.pass_context
@pass_configuration
def run_cli(  # pylint: disable=too-many-arguments
    configuration: Configuration,
    ctx: click.Context,
    sources: Sequence[Union[Path, str]],
    context: Optional[List[str]],
    allow: Optional[List[str]],
    deny: Optional[List[str]],
    previous: Optional[int],
    failed: bool,
    install: bool,
    cache: bool,
    verbosity: str,
    mode: Optional[str],
    output: Optional[str],
) -> None:
    """
    Run static code analysis commands on sources.

    Source files to run Statue on can be presented as positional arguments.
    When no source files are presented, will use configuration file to determine on
    which files to run
    """
    commands_map = None
    sources = __get_sources(sources, configuration)
    if len(sources) == 0:
        click.echo(
            '"Run" command cannot be run without a specified source '
            "or a sources section in Statue's configuration."
        )
        click.echo(
            'Please consider running "statue config init" in order to initialize '
            "default configuration."
        )
        ctx.exit(1)
    try:
        commands_map = __get_commands_map(
            configuration=configuration,
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
    if commands_map is None or len(commands_map) == 0:
        click.echo(ctx.get_help())
        return
    command_names = commands_map.command_names
    missing_commands = [
        command_builder
        for command_builder in configuration.commands_repository
        if command_builder.name in command_names
        and not command_builder.installed_correctly()
    ]
    __handle_missing_commands(
        ctx=ctx,
        missing_commands=missing_commands,
        install=install,
        verbosity=verbosity,
    )
    if mode is None:
        mode = configuration.default_mode.name
    if is_verbose(verbosity):
        click.echo(f"Running evaluation in {mode.lower()} mode")
    runner = build_runner(mode)
    with click.progressbar(
        length=commands_map.total_commands_count, show_pos=True, show_eta=False
    ) as bar:
        evaluation = runner.evaluate(
            commands_map=commands_map,
            update_func=lambda command: __bar_update_func(bar, command),
        )
    if not is_silent(verbosity):
        click.echo(boxed_string("Evaluation"))
        click.echo(evaluation_string(evaluation, verbosity=verbosity))
    if cache:
        configuration.cache.save_evaluation(evaluation)
    if output is not None:
        evaluation.save_as_json(output)
    click.echo()
    if not is_silent(verbosity):
        click.echo(boxed_string("Summary"))
        click.echo()
    ctx.exit(__print_evaluation_and_return_exit_code(evaluation))


def __get_sources(sources, configuration):
    if len(sources) == 0:
        return configuration.sources_repository.sources_list
    return [Path(source) for source in sources]


def __print_evaluation_and_return_exit_code(evaluation: Evaluation):
    if evaluation.success:
        click.echo(
            "Statue finished successfully after "
            f"{evaluation.total_execution_duration:.2f} seconds!"
        )
        return 0
    click.echo(
        f"Statue has failed after {evaluation.total_execution_duration:.2f} "
        "seconds on the following commands:"
    )
    click.echo()
    for source, source_evaluation in evaluation.failure_evaluation.items():
        click.echo(f"{source_style(source)}:")
        failed_commands_string = ", ".join(
            [
                name_style(command_evaluation.command.name)
                for command_evaluation in source_evaluation
            ]
        )
        click.echo(f"\t{failed_commands_string}")
    return 1


def __get_commands_map(  # pylint: disable=too-many-arguments
    configuration, sources, context, allow, deny, failed, previous
):
    if failed and previous is None:
        previous = 1
    if previous is None:
        allow = frozenset(allow) if len(allow) != 0 else None
        deny = frozenset(deny) if len(deny) != 0 else None
        context = frozenset(
            {
                configuration.contexts_repository[context_name]
                for context_name in context
            }
        )
        return configuration.build_commands_map(
            sources=sources,
            commands_filter=CommandsFilter(
                contexts=context, allowed_commands=allow, denied_commands=deny
            ),
        )
    evaluation_path = configuration.cache.evaluation_path(previous - 1)
    if evaluation_path is None or not evaluation_path.exists():
        return None
    evaluation = Evaluation.load_from_file(evaluation_path)
    if failed:
        return evaluation.failure_evaluation.commands_map
    return evaluation.commands_map


def __handle_missing_commands(ctx, missing_commands, install, verbosity):
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


def __bar_update_func(bar, partial_evaluation: Evaluation):
    bar.update(1)

    failures = failure_style(f"{partial_evaluation.failed_commands_number} failed")
    success = success_style(
        f"{partial_evaluation.successful_commands_number} succeeded"
    )
    bar.label = f"{failures}, {success}"
