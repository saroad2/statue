"""History CLI."""
import time

import click

from statue.cache import Cache
from statue.cli.cli import statue as statue_cli
from statue.constants import DATETIME_FORMAT
from statue.evaluation import Evaluation


@statue_cli.group("history")
def history_cli() -> None:
    """History related actions such as list, show, etc."""


@history_cli.command("list")
@click.option("--head", type=int, help="Show only the nth first evaluations")
def list_evaluations(head):
    """List all recent evaluations."""
    evaluation_paths = Cache.all_evaluation_paths()
    if len(evaluation_paths) == 0:
        click.echo("No previous evaluations.")
        return
    if head is not None:
        evaluation_paths = evaluation_paths[:head]
    for i, evaluation_path in enumerate(evaluation_paths, start=1):
        parsed_time = time.localtime(int(evaluation_path.stem.split("-")[-1]))
        time_string = time.strftime(DATETIME_FORMAT, parsed_time)
        evaluation = Evaluation.load_from_file(evaluation_path)
        success_ratio = (
            f"{evaluation.successful_commands_number}/{evaluation.commands_number}"
        )
        status = (
            click.style("Success", fg="green")
            if evaluation.success
            else click.style("Failure", fg="red")
        )
        click.echo(
            f"{i}) "
            f"{click.style(time_string, fg='yellow')} - "
            f"{status} ({success_ratio} successful)"
        )
