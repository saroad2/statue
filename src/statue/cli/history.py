"""History CLI."""
import time
from pathlib import Path
from typing import Union

import click

from statue.cache import Cache
from statue.cli.cli import statue_cli
from statue.cli.util import bullet_style, failure_style, success_style
from statue.constants import DATETIME_FORMAT
from statue.evaluation import CommandEvaluation, Evaluation


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
    parsed_time = time.localtime(int(evaluation_path.stem.split("-")[-1]))
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


def positive_validation(  # pylint: disable=unused-argument
    ctx: click.Context, param: click.Parameter, value: int
) -> int:
    """
    Validate number is 1 or greater.

    :param ctx: Unused context variable
    :type ctx: click.Context
    :param param: Unused parameter variable
    :type param: click.Parameter
    :param value: value to be validated
    :type value: int
    :return: Returns the value as it is.
    :rtype: int
    :raises BadParameter: Raised when parameter value is less then 1.
    """
    if value < 1:
        raise click.BadParameter(f"Number should be 1 or greater. got {value}")
    return value


@statue_cli.group("history")
def history_cli() -> None:
    """History related actions such as list, show, etc."""


@history_cli.command("list")
@click.option("--head", type=int, help="Show only the nth recent evaluations")
def list_evaluations_cli(head):
    """List all recent evaluations."""
    evaluation_paths = Cache.all_evaluation_paths()
    if len(evaluation_paths) == 0:
        click.echo("No previous evaluations.")
        return
    if head is not None:
        evaluation_paths = evaluation_paths[:head]
    for i, evaluation_path in enumerate(evaluation_paths, start=1):
        evaluation = Evaluation.load_from_file(evaluation_path)
        click.echo(
            f"{i}) "
            f"{evaluation_datetime(evaluation_path)} - {evaluation_status(evaluation)} "
            f"({evaluation_success_ratio(evaluation)} successful)"
        )


@history_cli.command("show")
@click.option(
    "-n",
    "number",
    type=int,
    default=1,
    callback=positive_validation,
    help="Show nth recent evaluation. 1 by default",
)
def show_evaluation_cli(number):
    """Show past evaluation."""
    evaluation_path = Cache.evaluation_path(number - 1)
    evaluation = Evaluation.load_from_file(evaluation_path)
    click.echo(
        f"{evaluation_datetime(evaluation_path)} - {evaluation_status(evaluation)} "
        f"({evaluation_success_ratio(evaluation)} successful)"
    )
    for source, source_evaluation in evaluation.items():
        click.echo(f"{source}:")
        for command_evaluation in source_evaluation.commands_evaluations:
            click.echo(
                f"\t{command_evaluation.command.name} - "
                f"{evaluation_status(command_evaluation)}"
            )


@history_cli.command("clear")
@click.option("-f", "--force", is_flag=True, help="Force deletion and avoid prompt.")
@click.option(
    "-l",
    "--limit",
    type=int,
    help="Limit the number of deleted records. Deletes earliest evaluations.",
)
def clear_history_cli(force, limit):
    """Clear records of previous statue runs."""
    evaluation_files = Cache.all_evaluation_paths()
    number_of_evaluation_files = len(evaluation_files)
    if number_of_evaluation_files == 0:
        click.echo("No previous evaluations.")
        return
    if limit and limit < number_of_evaluation_files:
        evaluation_files = evaluation_files[-limit:]
        number_of_evaluation_files = limit
    if not force:
        confirmation = click.confirm(
            f"{number_of_evaluation_files} evaluation files are bout to be deleted. "
            "Are you wish to delete those?",
            default=False,
        )
        if not confirmation:
            click.echo("Aborted without clearing history.")
            return
    for evaluation_file in evaluation_files:
        evaluation_file.unlink()
