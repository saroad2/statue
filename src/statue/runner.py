"""Command map runner."""
import time
from typing import Callable, Dict, List, Optional

from statue.command import Command
from statue.evaluation import Evaluation, SourceEvaluation


def evaluate_commands_map(
    commands_map: Dict[str, List[Command]],
    update_func: Optional[Callable[[Evaluation], None]] = None,
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
    total_start_time = time.time()
    for source, commands in commands_map.items():
        source_start_time = time.time()
        evaluation[source] = SourceEvaluation()
        for command in commands:
            evaluation[source].append(command.execute(source))
            if update_func is not None:
                update_func(evaluation)
        source_end_time = time.time()
        evaluation[source].source_execution_duration = (
            source_end_time - source_start_time
        )
    total_end_time = time.time()
    evaluation.total_execution_duration = total_end_time - total_start_time
    return evaluation
