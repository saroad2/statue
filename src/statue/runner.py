"""Command map runner."""
import time
from typing import Callable, Optional

from statue.commands_map import CommandsMap
from statue.evaluation import Evaluation, SourceEvaluation


class SynchronousEvaluationRunner:  # pylint: disable=too-few-public-methods
    """Runner class for running command synchronously."""

    @classmethod
    def evaluate(
        cls,
        commands_map: CommandsMap,
        update_func: Optional[Callable[[Evaluation], None]] = None,
    ) -> Evaluation:
        """
        Run commands map and return evaluation report.

        :param commands_map: map from input file to list of commands to run on it
        :type commands_map: CommandsMap
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
