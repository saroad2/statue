"""Command map runner."""
import abc
import asyncio
import time
from enum import Enum, auto
from typing import Callable, List, Optional

from statue.command import Command
from statue.commands_map import CommandsMap
from statue.evaluation import Evaluation, SourceEvaluation


class RunnerMode(Enum):
    """Enum indicating in which mode are we running evaluation."""

    SYNC = auto()
    ASYNC = auto()


class EvaluationRunner:  # pylint: disable=too-few-public-methods
    """Evaluation runner interface."""

    @abc.abstractmethod
    def evaluate(
        self,
        commands_map: CommandsMap,
        update_func: Optional[Callable[[Evaluation], None]] = None,
    ) -> Evaluation:
        """
        Abstract evaluation method.

        # noqa: DAR202

        :param commands_map: map from source file to list of commands to run on it
        :type commands_map: CommandsMap
        :param update_func: Function to be called before every command is
            executed. Skip if None
        :type update_func: Optional[Callable[[Command], None]]
        :return: Total evaluation after running all commands.
        :rtype: Evaluation
        """
        ...


class SynchronousEvaluationRunner(  # pylint: disable=too-few-public-methods
    EvaluationRunner
):
    """Runner class for running commands synchronously."""

    def evaluate(
        self,
        commands_map: CommandsMap,
        update_func: Optional[Callable[[Evaluation], None]] = None,
    ) -> Evaluation:
        """
        Run commands map and return evaluation report.

        :param commands_map: map from source file to list of commands to run on it
        :type commands_map: CommandsMap
        :param update_func: Function to be called before every command is
            executed. Skip if None
        :type update_func: Optional[Callable[[Command], None]]
        :return: Total evaluation after running all commands.
        :rtype: Evaluation
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


class AsynchronousEvaluationRunner(EvaluationRunner):
    """Runner class for running commands asynchronously."""

    def __init__(self):
        """Initialize runner."""
        self.update_lock = asyncio.Lock()

    def evaluate(
        self,
        commands_map: CommandsMap,
        update_func: Optional[Callable[[Evaluation], None]] = None,
    ) -> Evaluation:
        """
        Run commands map asynchronously and return evaluation report.

        :param commands_map: map from source file to list of commands to run on it
        :type commands_map: CommandsMap
        :param update_func: Function to be called before every command is
            executed. Skip if None
        :type update_func: Optional[Callable[[Command], None]]
        :return: Total evaluation after running all commands.
        :rtype: Evaluation
        """
        return asyncio.run(
            self.evaluate_commands_map(
                commands_map=commands_map, update_func=update_func
            )
        )

    async def evaluate_commands_map(
        self,
        commands_map: CommandsMap,
        update_func: Optional[Callable[[Evaluation], None]] = None,
    ):
        """
        Main async function to run commands map and return evaluation report.

        :param commands_map: map from source file to list of commands to run on it
        :type commands_map: CommandsMap
        :param update_func: Function to be called before every command is
            executed. Skip if None
        :type update_func: Optional[Callable[[Command], None]]
        :return: Evaluation
        """
        evaluation = Evaluation()
        start_time = time.time()
        coros = [
            self.evaluate_source(
                source=source,
                commands=commands,
                evaluation=evaluation,
                update_func=update_func,
            )
            for source, commands in commands_map.items()
        ]
        await asyncio.gather(*coros)
        end_time = time.time()
        evaluation.total_execution_duration = end_time - start_time
        return evaluation

    async def evaluate_source(
        self,
        source: str,
        commands: List[Command],
        evaluation: Evaluation,
        update_func: Optional[Callable[[Evaluation], None]] = None,
    ):
        """
        Evaluate commands on source and return source evaluation report.

        :param source: Path of the desired source.
        :type source: str
        :param commands: List of commands to run on the source.
        :type commands: List[Command]
        :param evaluation: Evaluation instance to be updated after commands are running.
        :type evaluation: Evaluation
        :param update_func: Function to be called before every command is
            executed. Skip if None
        :type update_func: Optional[Callable[[Command], None]]
        """
        evaluation[source] = SourceEvaluation()
        start_time = time.time()
        coros = [
            self.evaluate_command(
                command=command,
                source=source,
                evaluation=evaluation,
                update_func=update_func,
            )
            for command in commands
        ]
        await asyncio.gather(*coros)
        end_time = time.time()
        evaluation[source].source_execution_duration = end_time - start_time

    async def evaluate_command(
        self,
        command: Command,
        source: str,
        evaluation: Evaluation,
        update_func: Optional[Callable[[Evaluation], None]] = None,
    ):
        """
        Evaluate command on source and return command evaluation report.

        :param source: Path of the desired source.
        :type source: str
        :param command: Command to run on the source.
        :type command: Command
        :param evaluation: Evaluation instance to be updated after commands are running.
        :type evaluation: Evaluation
        :param update_func: Function to be called before every command is
            executed. Skip if None
        :type update_func: Optional[Callable[[Command], None]]
        """
        command_evaluation = await command.execute_async(source)
        await self.update_lock.acquire()
        evaluation[source].append(command_evaluation)
        if update_func is not None:
            update_func(evaluation)
        self.update_lock.release()


MODE_TO_RUNNER_DICT = {
    RunnerMode.SYNC.name: SynchronousEvaluationRunner,
    RunnerMode.ASYNC.name: AsynchronousEvaluationRunner,
}


def build_runner(runner_mode: str) -> EvaluationRunner:
    """
    Build commands runner.

    :param runner_mode: Which mode should the runner work in
    :type runner_mode: str
    :return: Runner instance.
    :rtype: EvaluationRunner
    """
    return MODE_TO_RUNNER_DICT[runner_mode]()
