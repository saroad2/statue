"""History CLI."""
import sys
from datetime import datetime
from typing import Optional, Union

import click

from statue.cli.cli import pass_configuration, statue_cli
from statue.cli.common_flags import verbose_option
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
from statue.exceptions import CacheError
from statue.verbosity import is_verbose


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


def evaluation_success_ratio(evaluation: Evaluation) -> str:
    """
    Get evaluation ratio string.

    :param evaluation: The evaluation to get the status of
    :type evaluation: Evaluation
    :return: success ratio string
    :rtype: str
    """
    return f"{evaluation.successful_commands_number}/{evaluation.commands_number}"


def total_evaluation_string(evaluation: Evaluation) -> str:
    """
    Create a string representing an evaluation.

    :param evaluation: The actual evaluation instance.
    :type evaluation: Evaluation
    :return: Pretty string describing the evaluation
    :rtype: str
    """
    return (
        f"{bullet_style(datetime.strftime(evaluation.timestamp, DATETIME_FORMAT))} -"
        f" {evaluation_status(evaluation)} "
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
    evaluations = configuration.cache.all_evaluations
    if len(evaluations) == 0:
        click.echo("No previous evaluations.")
        return
    if head is not None:
        evaluations = evaluations[:head]
    for i, evaluation in enumerate(evaluations, start=1):
        click.echo(f"{i}) {total_evaluation_string(evaluation)}")


@history_cli.command("show")
@click.option(
    "-n", "number", type=int, default=1, help="Show nth recent evaluation. 1 by default"
)
@pass_configuration
@verbose_option
def show_evaluation_cli(
    configuration: Configuration,
    number: int,
    verbosity: str,
):
    """Show past evaluation."""
    try:
        evaluation = configuration.cache.get_evaluation(number - 1)
    except CacheError:
        click.echo(
            failure_style(f"Could not find evaluation with given index {number}")
        )
        sys.exit(1)
    click.echo(total_evaluation_string(evaluation))
    for source, source_evaluation in evaluation.items():
        click.echo(
            f"{source_style(str(source))} ("
            f"{source_evaluation.source_execution_duration:.2f} seconds):"
        )
        for command_evaluation in source_evaluation.commands_evaluations:
            click.echo(
                f"\t{name_style(command_evaluation.command.name)} - "
                f"{evaluation_status(command_evaluation)} "
                f"({command_evaluation.execution_duration:.2f} seconds)"
            )
            if is_verbose(verbosity):
                click.echo(
                    f"\t\tArguments: {' '.join(command_evaluation.command.args)}"
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
def clear_history_cli(configuration: Configuration, force: bool, limit: Optional[int]):
    """Clear records of previous statue runs."""
    number_of_evaluations = configuration.cache.number_of_evaluations
    if number_of_evaluations == 0:
        click.echo("No previous evaluations.")
        return
    number_of_files_to_be_deleted = (
        limit if limit is not None else number_of_evaluations
    )
    if not force:
        confirmation = click.confirm(
            f"{number_of_files_to_be_deleted} evaluation files are "
            "about to be deleted. Are you sure you want to delete them?",
            default=False,
        )
        if not confirmation:
            click.echo("Aborted without clearing history.")
            return
    configuration.cache.clear(limit=limit)
    click.echo(
        f"{number_of_files_to_be_deleted} evaluation files "
        "have been deleted successfully."
    )
