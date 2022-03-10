# noqa: D100
# pylint: disable=missing-module-docstring
import asyncio
import os
import subprocess  # nosec
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Union

from statue.constants import ENCODING
from statue.exceptions import CommandExecutionError
from statue.sources_locks_repository import SourcesLocksRepository


@dataclass
class CommandEvaluation:
    """Evaluation result of a command."""

    command: "Command"
    success: bool
    execution_duration: float
    captured_output: List[str] = field(default_factory=list)

    @property
    def captured_output_string(self):
        """Join captured output into a single string."""
        return "\n".join(self.captured_output)

    def as_json(self) -> Dict[str, Any]:
        """
        Return command evaluation as json dictionary.

        :return: Self as dictionary
        :rtype: Dict[str, Any]
        """
        command_json = {
            key: value
            for key, value in asdict(self.command).items()
            if value is not None
        }
        return dict(
            command=command_json,
            execution_duration=self.execution_duration,
            captured_output=self.captured_output,
            success=self.success,
        )

    @classmethod
    def from_json(cls, command_evaluation: Dict[str, Any]) -> "CommandEvaluation":
        """
        Read command evaluation from json dictionary.

        :param command_evaluation: Json command evaluation
        :type command_evaluation: Dict[str, Any]
        :return: Parsed command evaluation
        :rtype: CommandEvaluation
        """
        return CommandEvaluation(
            command=Command(**command_evaluation["command"]),
            success=command_evaluation["success"],
            execution_duration=command_evaluation["execution_duration"],
            captured_output=command_evaluation["captured_output"],
        )


@dataclass
class Command:
    """Runnable evaluation command."""

    name: str
    args: List[str] = field(default_factory=list)

    def program_execution_args(self, source: Union[Path, str]) -> List[str]:
        """
        Get the program command to be run as a subprocess.

        :param source: The source to run the command on.
        :type source: Union[Path, str]
        :return: Program arguments list
        :rtype: List[str]
        """
        return [self.name, str(source), *self.args]

    def execute(self, source: str) -> CommandEvaluation:
        """
        Execute the command.

        :param source: source files to check.
        :type: str
        :return: Command's evaluation including the command itself and is it successful
        :rtype: CommandEvaluation
        :raises CommandExecutionError: raised when command is not found.
        """
        try:
            start_time = time.time()
            subprocess_result = subprocess.run(
                self.program_execution_args(source),
                env=os.environ,
                check=False,
                capture_output=True,
            )
            end_time = time.time()
        except FileNotFoundError as error:
            raise CommandExecutionError(self.name) from error
        captured_stdout = subprocess_result.stdout.decode(ENCODING)
        captured_stderr = subprocess_result.stderr.decode(ENCODING)
        return CommandEvaluation(
            command=self,
            success=(subprocess_result.returncode == 0),
            execution_duration=end_time - start_time,
            captured_output=self._build_captured_output(
                captured_stdout=captured_stdout, captured_stderr=captured_stderr
            ),
        )

    async def execute_async(self, source) -> CommandEvaluation:
        """
        Execute the command asynchronously.

        :param source: source files to check.
        :type: str
        :return: Command's evaluation including the command itself and is it successful
        :rtype: CommandEvaluation
        :raises CommandExecutionError: raised when command is not found.
        """
        source_lock = await SourcesLocksRepository.get_lock(source)
        try:
            await source_lock.acquire()
            start_time = time.time()
            async_process = await asyncio.create_subprocess_exec(
                *self.program_execution_args(source),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                env=os.environ,
            )
            stdout, stderr = await async_process.communicate()
            end_time = time.time()
            source_lock.release()
        except FileNotFoundError as error:
            raise CommandExecutionError(self.name) from error
        captured_stdout, captured_stderr = stdout.decode(ENCODING), stderr.decode(
            ENCODING
        )
        return CommandEvaluation(
            command=self,
            success=(async_process.returncode == 0),
            execution_duration=end_time - start_time,
            captured_output=self._build_captured_output(
                captured_stdout=captured_stdout, captured_stderr=captured_stderr
            ),
        )

    @classmethod
    def _build_captured_output(cls, captured_stdout, captured_stderr):
        captured_output_as_string = captured_stdout + captured_stderr
        return (
            captured_output_as_string.split("\n")
            if len(captured_output_as_string) != 0
            else []
        )
