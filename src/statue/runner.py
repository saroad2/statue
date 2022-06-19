"""Command map runner."""
import abc
import asyncio
import time
from enum import Enum, auto
from pathlib import Path
from typing import List

import tqdm

from statue.command import Command
from statue.commands_map import CommandsMap
from statue.constants import BAR_FORMAT, MAIN_BAR_COLOR, SECONDARY_BAR_COLOR
from statue.evaluation import Evaluation, SourceEvaluation


class RunnerMode(Enum):
    """Enum indicating in which mode are we running evaluation."""

    SYNC = auto()
    ASYNC = auto()
    DEFAULT_MODE = SYNC


class EvaluationRunner:  # pylint: disable=too-few-public-methods
    """Evaluation runner interface."""

    @abc.abstractmethod
    def evaluate(
        self,
        commands_map: CommandsMap,
    ) -> Evaluation:
        """
        Abstract evaluation method.

        # noqa: DAR202

        :param commands_map: map from source file to list of commands to run on it
        :type commands_map: CommandsMap
        :return: Total evaluation after running all commands.
        :rtype: Evaluation
        """


class SynchronousEvaluationRunner(  # pylint: disable=too-few-public-methods
    EvaluationRunner
):
    """Runner class for running commands synchronously."""

    def evaluate(
        self,
        commands_map: CommandsMap,
    ) -> Evaluation:
        """
        Run commands map and return evaluation report.

        :param commands_map: map from source file to list of commands to run on it
        :type commands_map: CommandsMap
        :return: Total evaluation after running all commands.
        :rtype: Evaluation
        """
        evaluation = Evaluation()
        total_start_time = time.time()
        with tqdm.trange(
            commands_map.total_commands_count,
            bar_format=BAR_FORMAT,
            colour=MAIN_BAR_COLOR,
        ) as main_bar:
            for source, commands in commands_map.items():
                source_start_time = time.time()
                evaluation[source] = SourceEvaluation()
                for command in tqdm.tqdm(
                    commands,
                    bar_format=BAR_FORMAT,
                    colour=SECONDARY_BAR_COLOR,
                    leave=False,
                    desc=str(source),
                ):
                    evaluation[source].append(command.execute(source))
                    main_bar.update(1)
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
    ) -> Evaluation:
        """
        Run commands map asynchronously and return evaluation report.

        :param commands_map: map from source file to list of commands to run on it
        :type commands_map: CommandsMap
        :return: Total evaluation after running all commands.
        :rtype: Evaluation
        """
        return asyncio.run(self.evaluate_commands_map(commands_map))

    async def evaluate_commands_map(
        self,
        commands_map: CommandsMap,
    ):
        """
        Main async function to run commands map and return evaluation report.

        :param commands_map: map from source file to list of commands to run on it
        :type commands_map: CommandsMap
        :return: Evaluation
        """
        evaluation = Evaluation()
        start_time = time.time()
        max_source_name_length = max(
            len(source.as_posix()) for source in commands_map.keys()
        )
        with tqdm.trange(
            commands_map.total_commands_count,
            bar_format=BAR_FORMAT,
            colour=MAIN_BAR_COLOR,
        ) as main_bar:
            coros = [
                self.evaluate_source(
                    source_bar_pos=pos,
                    source=source,
                    commands=commands,
                    evaluation=evaluation,
                    main_bar=main_bar,
                    max_source_name_length=max_source_name_length,
                )
                for pos, (source, commands) in enumerate(commands_map.items(), start=1)
            ]
            await asyncio.gather(*coros)
        end_time = time.time()
        evaluation.total_execution_duration = end_time - start_time
        return evaluation

    async def evaluate_source(  # pylint: disable=too-many-arguments
        self,
        source: Path,
        commands: List[Command],
        evaluation: Evaluation,
        main_bar: tqdm.tqdm,
        source_bar_pos: int,
        max_source_name_length: int,
    ):
        """
        Evaluate commands on source and return source evaluation report.

        :param source_bar_pos: Position of the source bar to print
        :type source_bar_pos: int
        :param source: Path of the desired source.
        :type source: Path
        :param commands: List of commands to run on the source.
        :type commands: List[Command]
        :param evaluation: Evaluation instance to be updated after commands are running.
        :type evaluation: Evaluation
        :param main_bar: progress bar that shows how far are we in evaluating the source
        :type main_bar: tqdm.tqdm
        :param max_source_name_length: Maximum source name length
        :type max_source_name_length: int
        """
        evaluation[source] = SourceEvaluation()
        start_time = time.time()
        with tqdm.trange(
            len(commands),
            bar_format=BAR_FORMAT,
            position=source_bar_pos,
            leave=False,
            colour=SECONDARY_BAR_COLOR,
            desc=f"{source.as_posix():{max_source_name_length}}",
        ) as source_bar:
            coros = [
                self.evaluate_command(
                    command=command,
                    source=source,
                    evaluation=evaluation,
                    source_bar=source_bar,
                    main_bar=main_bar,
                )
                for command in commands
            ]
            await asyncio.gather(*coros)
        end_time = time.time()
        evaluation[source].source_execution_duration = end_time - start_time
        await self.update_lock.acquire()
        self.update_lock.release()

    async def evaluate_command(  # pylint: disable=too-many-arguments
        self,
        command: Command,
        source: Path,
        evaluation: Evaluation,
        source_bar: tqdm.tqdm,
        main_bar: tqdm.tqdm,
    ):
        """
        Evaluate command on source and return command evaluation report.

        :param source: Path of the desired source.
        :type source: Path
        :param command: Command to run on the source.
        :type command: Command
        :param evaluation: Evaluation instance to be updated after commands are running.
        :type evaluation: Evaluation
        :param source_bar: tqdm progress bar to show the progress
            of evaluating this specific source.
        :type source_bar: tqdm.tqdm
        :param main_bar: tqdm progress bar to show total progress
        :type main_bar: tqdm.tqdm
        """
        command_evaluation = await command.execute_async(source)
        await self.update_lock.acquire()
        evaluation[source].append(command_evaluation)
        source_bar.update(1)
        main_bar.update(1)
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
