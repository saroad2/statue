"""Command map runner."""
from typing import Callable, Dict, List, Optional

from statue.command import Command
from statue.evaluation import Evaluation, SourceEvaluation


def evaluate_commands_map(
    commands_map: Dict[str, List[Command]],
    update_func: Optional[Callable[[Command], None]] = None,
) -> Evaluation:
    """
    Run commands map and return evaluation report.

    :param commands_map: map from input file to list of commands to run on it,
    :type commands_map: Dict[str, List[Command]],
    :param update_func: Function to be called before every command is
        executed. Skip if None
    :type update_func: Optional[Callable[[Command], None]]
    :return: Evaluation
    """
    evaluation = Evaluation()
    for input_path, commands in commands_map.items():
        source_evaluation = SourceEvaluation()
        for command in commands:
            if update_func is not None:
                update_func(command)
            source_evaluation.commands_evaluations.append(command.execute(input_path))
        evaluation[input_path] = source_evaluation
    return evaluation
