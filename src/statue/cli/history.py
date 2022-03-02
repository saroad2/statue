"""History CLI."""
import time
from pathlib import Path
from typing import Union

import click

from statue.cache import Cache
from statue.cli.cli import pass_configuration, statue_cli
from statue.cli.styled_strings import (
    bullet_style,
    failure_style,
    name_style,
    source_style,
    success_style,
)
from statue.command import CommandEvaluation
from statue.config.configuration import Configuration
from statue.constants import DATETIME_FORMAT
from statue.evaluation import Evaluation


def evaluation_status(evaluation: Union[Evaluation, CommandEvaluation]) -> str:
    """
    Get styled evaluation string.

    :param evaluation: The evaluation to get the status of
    :type evaluation: Evaluation or CommandEvaluation
    :return: styles success/failure string
    :rtype: str
    """
    if evaluation.success:
        return success_style("Success")
    return failure_style("Failure")


def evaluation_datetime(evaluation_path: Path) -> str:
    """
    Get styled time string for evaluation path.

    :param evaluation_path: The path where the evaluation is saved
    :type evaluation_path: Path
    :return: styles datetime string
    :rtype: str
    """
    evaluation_time_stamp = Cache.extract_time_stamp_from_path(evaluation_path)
    parsed_time = time.localtime(evaluation_time_stamp)
    return bullet_style(time.strftime(DATETIME_FORMAT, parsed_time))


def evaluation_success_ratio(evaluation: Evaluation) -> str:
    """
    Get evaluation ratio string.

    :param evaluation: The evaluation to get the status of
    :type evaluation: Evaluation
    :return: success ratio string
    :rtype: str
    """
    return f"{evaluation.successful_commands_number}/{evaluation.commands_number}"


def total_evaluation_string(evaluation_path: Path, evaluation: Evaluation) -> str:
    """
    Create a string representing an evaluation.

    :param evaluation_path: Path of a given evaluation.
    :type evaluation_path: Path
    :param evaluation: The actual evaluation instance.
    :type evaluation: Evaluation
    :return: Pretty string describing the evaluation
    :rtype: str
    """
    return (
        f"{evaluation_datetime(evaluation_path)} - {evaluation_status(evaluation)} "
        f"({evaluation_success_ratio(evaluation)} successful, "
        f"{evaluation.total_execution_duration:.2f} seconds)"
    )


@statue_cli.group("history")
def history_cli() -> None:
    """History related actions such as list, show, etc."""


@history_cli.command("list")
@click.option("--head", type=int, help="Show only the nth recent evaluations")
@pass_configuration
def list_evaluations_cli(configuration: Configuration, head: int):
    """List all recent evaluations."""
    evaluation_paths = configuration.cache.all_evaluation_paths
    if len(evaluation_paths) == 0:
        click.echo("No previous evaluations.")
        return
    if head is not None:
        evaluation_paths = evaluation_paths[:head]
    for i, evaluation_path in enumerate(evaluation_paths, start=1):
        evaluation = Evaluation.load_from_file(evaluation_path)
        click.echo(f"{i}) {total_evaluation_string(evaluation_path, evaluation)}")


@history_cli.command("show")
@click.option(
    "-n", "number", type=int, default=1, help="Show nth recent evaluation. 1 by default"
)
@click.pass_context
@pass_configuration
def show_evaluation_cli(configuration: Configuration, ctx: click.Context, number: int):
    """Show past evaluation."""
    evaluation_path = None
    try:
        evaluation_path = configuration.cache.evaluation_path(number - 1)
    except IndexError:
        click.echo(
            failure_style(f"Could not find evaluation with given index {number}")
        )
        ctx.exit(1)
    evaluation = Evaluation.load_from_file(evaluation_path)
    click.echo(total_evaluation_string(evaluation_path, evaluation))
    for source, source_evaluation in evaluation.items():
        click.echo(
            f"{source_style(source)} ("
            f"{source_evaluation.source_execution_duration:.2f} seconds):"
        )
        for command_evaluation in source_evaluation.commands_evaluations:
            click.echo(
                f"\t{name_style(command_evaluation.command.name)} - "
                f"{evaluation_status(command_evaluation)} "
                f"({command_evaluation.execution_duration:.2f} seconds)"
            )


@history_cli.command("clear")
@click.option("-f", "--force", is_flag=True, help="Force deletion and avoid prompt.")
@click.option(
    "-l",
    "--limit",
    type=int,
    help="Limit the number of deleted records. Deletes earliest evaluations.",
)
@pass_configuration
def clear_history_cli(configuration: Configuration, force: bool, limit: int):
    """Clear records of previous statue runs."""
    evaluation_files = configuration.cache.all_evaluation_paths
    number_of_evaluation_files = len(evaluation_files)
    if number_of_evaluation_files == 0:
        click.echo("No previous evaluations.")
        return
    if limit and limit < number_of_evaluation_files:
        evaluation_files = evaluation_files[-limit:]
        number_of_evaluation_files = limit
    if not force:
        confirmation = click.confirm(
            f"{number_of_evaluation_files} evaluation files are about to be deleted. "
            "Are you wish to delete those?",
            default=False,
        )
        if not confirmation:
            click.echo("Aborted without clearing history.")
            return
    for evaluation_file in evaluation_files:
        evaluation_file.unlink()
    click.echo(
        f"{number_of_evaluation_files} evaluation files have been deleted successfully."
    )
