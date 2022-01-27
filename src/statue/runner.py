"""Command map runner."""
from typing import Callable, Dict, List

from statue.command import Command
from statue.evaluation import Evaluation, SourceEvaluation
from statue.print_util import print_title
from statue.verbosity import DEFAULT_VERBOSITY, is_silent


def evaluate_commands_map(
    commands_map: Dict[str, List[Command]],
    verbosity: str = DEFAULT_VERBOSITY,
    print_method: Callable[..., None] = print,
) -> Evaluation:
    """
    Run commands map and return evaluation report.

    :param commands_map: map from input file to list of commands to run on it,
    :type commands_map: Dict[str, List[Command]],
    :param verbosity: verbosity level
    :type verbosity: str
    :param print_method: print method, can be either ``print`` or ``click.echo``
    :type print_method: Callable
    :return: Evaluation
    """
    evaluation = Evaluation()
    for input_path, commands in commands_map.items():
        source_evaluation = SourceEvaluation()
        if not is_silent(verbosity):
            print_method("")
            print_method("")
            print_title(input_path, transform=False, print_method=print_method)
            print_method("")
        for command in commands:
            if not is_silent(verbosity):
                print_title(command.name, underline="-", print_method=print_method)
            source_evaluation.commands_evaluations.append(
                command.execute(input_path, verbosity)
            )
        evaluation[input_path] = source_evaluation
    return evaluation
