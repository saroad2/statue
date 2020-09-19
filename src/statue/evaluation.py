"""Evaluation of commands map."""
from typing import Callable, Dict, List

from statue.command import Command
from statue.print_util import print_title
from statue.verbosity import DEFAULT_VERBOSITY, is_silent


def evaluate_commands_map(
    commands_map: Dict[str, List[Command]],
    verbosity: str = DEFAULT_VERBOSITY,
    print_method: Callable[..., None] = print,
) -> Dict[str, List[str]]:
    """
    Run commands map and return evaluation report.

    :param commands_map: map from input file to list of commands to run on it,
    :param verbosity: verbosity level
    :param print_method: print method, can be either ``print`` or ``click.echo``
    :return: map from source to failed commands
    """
    failed_paths = dict()
    for input_path, commands in commands_map.items():
        if not is_silent(verbosity):
            print_method()
            print_method(f"Evaluating {input_path}")
        failed_commands = []
        for command in commands:
            if not is_silent(verbosity):
                print_title(command.name, underline="-")
            return_code = command.execute(input_path, verbosity)
            if return_code != 0:
                failed_commands.append(command.name)
        if len(failed_commands) != 0:
            failed_paths[input_path] = failed_commands
    return failed_paths
