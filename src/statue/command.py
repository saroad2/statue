# noqa: D100
# pylint: disable=missing-module-docstring
import importlib
import os
import subprocess  # nosec
import sys
import time
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional

import pkg_resources

from statue.constants import ENCODING
from statue.exceptions import CommandExecutionError
from statue.verbosity import DEFAULT_VERBOSITY, is_silent


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
    """
    Data class representing a command to run in order to evaluate the code.

    :param name: The name of the command to run.
    :param args: A list of arguments for the command.
    :param help: Help string
    :param version: One can specify a specific version of the command to use
    """

    name: str
    help: str
    args: List[str] = field(default_factory=list)
    version: Optional[str] = field(default=None)

    @property
    def install_name(self) -> str:
        """
        Name to state while installing with pip.

        When installing a specific version with pip, one should add "==" with the
        specific version afterwards.

        If no version is specified, same as name.

        :return: name and version
        :rtype: str
        """
        if self.version is None:
            return self.name
        return f"{self.name}=={self.version}"

    @property
    def installed_version(self) -> Optional[str]:
        """
        Version of the installed package.

        Might not be the same as the version attribute.

        :return: version of installed package
        :rtype: str or None
        """
        package = self._get_package()
        if package is None:
            return None
        return package.version

    def installed(self) -> bool:
        """
        Is this command installed.

        :return: Either the command is installed or not
        :rtype: bool
        """
        return self.installed_version is not None

    def installed_correctly(self) -> bool:
        """
        Checks that command is installed and its version matches.

        :return: whether the command is installed correctly
        :rtype: bool
        """
        return self.installed() and self.installed_version_match()

    def installed_version_match(self) -> bool:
        """
        Is the installed version match the specified version.

        :return: is the installed version matches the desired version
        :rtype: bool
        """
        if self.version is None:
            return True
        return self.installed_version == self.version

    def install(self, verbosity: str = DEFAULT_VERBOSITY) -> None:
        """
        Install command using pip.

        :param verbosity: Verbosity level.
        :type verbosity: str
        """
        if self.installed():
            return
        if not is_silent(verbosity):
            print(f"Installing {self.install_name}")
        subprocess.run(  # nosec
            [sys.executable, "-m", "pip", "install", self.install_name],
            env=os.environ,
            check=False,
            capture_output=is_silent(verbosity),
        )

    def update(self, verbosity: str = DEFAULT_VERBOSITY) -> None:
        """
        Update command using pip.

        :param verbosity: Verbosity level.
        :type verbosity: str
        """
        if not is_silent(verbosity):
            print(f"Updating {self.name}")
        subprocess.run(  # nosec
            [sys.executable, "-m", "pip", "install", "-U", self.name],
            env=os.environ,
            check=False,
            capture_output=is_silent(verbosity),
        )

    def uninstall(self, verbosity: str = DEFAULT_VERBOSITY) -> None:
        """
        Uninstall command using pip.

        :param verbosity: Verbosity level.
        :type verbosity: str
        """
        if not self.installed():
            return
        if not is_silent(verbosity):
            print(f"Uninstalling {self.name} (version {self.installed_version})")
        subprocess.run(  # nosec
            [sys.executable, "-m", "pip", "uninstall", "-y", self.name],
            env=os.environ,
            check=False,
            capture_output=is_silent(verbosity),
        )

    def update_to_version(self, verbosity=DEFAULT_VERBOSITY) -> None:
        """
        Update command to the specified version using pip.

        If the installed version is the same as version, do nothing.

        :param verbosity: Verbosity level.
        :type verbosity: str
        """
        if not self.installed():
            self.install(verbosity=verbosity)
            return
        if self.version is None:
            # If no version is specified, we update package to its latest version
            self.update(verbosity=verbosity)
            return
        if self.installed_version_match():
            return
        # If a version is specified, we must first uninstall it
        # before installing the specified version.
        self.uninstall(verbosity=verbosity)
        self.install(verbosity=verbosity)

    def execute(  # pylint: disable=too-many-arguments
        self, source: str
    ) -> CommandEvaluation:
        """
        Execute the command.

        :param source: source files to check.
        :type: str
        :return: Command's evaluation including the command itself and is it successful
        :rtype: CommandEvaluation
        """
        start_time = time.time()
        subprocess_result = self._run_subprocess(args=[self.name, source, *self.args])
        end_time = time.time()
        return CommandEvaluation(
            command=self,
            success=(subprocess_result.returncode == 0),
            execution_duration=end_time - start_time,
            captured_output=self._build_captured_output(subprocess_result),
        )

    def _run_subprocess(self, args: List[str]) -> subprocess.CompletedProcess:
        try:
            return subprocess.run(  # nosec
                args, env=os.environ, check=False, capture_output=True
            )
        except FileNotFoundError as error:
            raise CommandExecutionError(self.name) from error

    @classmethod
    def _build_captured_output(cls, subprocess_result):
        captured_stdout = subprocess_result.stdout.decode(ENCODING)
        captured_stderr = subprocess_result.stderr.decode(ENCODING)
        captured_output_as_string = (
            captured_stderr if len(captured_stderr) != 0 else captured_stdout
        )
        return (
            captured_output_as_string.split("\n")
            if len(captured_output_as_string) != 0
            else []
        )

    def _get_package(self):  # pragma: no cover
        """
        Get package of the desired command.

        If package is not installed, returns None.

        :return: self package
        """
        importlib.reload(pkg_resources)
        for package in list(pkg_resources.working_set):
            if package.key == self.name:
                return package
        return None
