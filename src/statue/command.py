# noqa: D100
# pylint: disable=missing-module-docstring
import os
import subprocess  # nosec
import sys
from dataclasses import dataclass, field
from typing import List

import pkg_resources

from statue.verbosity import DEFAULT_VERBOSITY, is_silent, is_verbose


@dataclass
class Command:
    """
    Data class representing a command to run in order to evaluate the code.

    :param name: The name of the command to run.
    :param args: A list of arguments for the command.
    :param help: Help string
    """

    name: str
    help: str
    args: List[str] = field(default_factory=list)

    def installed(self) -> bool:
        """
        Is this command installed.

        :return: Boolean.
        """
        return self.name in {
            pkg.key for pkg in self.available_packages()  # type: ignore
        }

    @classmethod
    def available_packages(cls):  # type: ignore
        """Get all available packages via pip."""
        return list(pkg_resources.working_set)  # pragma: no cover

    def install(self, verbosity: str = DEFAULT_VERBOSITY) -> None:
        """
        Install command using pip.

        :param verbosity: String. Verbosity level.
        """
        if not is_silent(verbosity):
            print(f"Installing {self.name}")
        subprocess.run(  # nosec
            [sys.executable, "-m", "pip", "install", self.name],
            env=os.environ,
            check=False,
            capture_output=is_silent(verbosity),
        )

    def execute(  # pylint: disable=too-many-arguments
        self,
        source: str,
        verbosity: str = DEFAULT_VERBOSITY,
    ) -> int:
        """
        Execute the command.

        :param source: source files to check.
        :param verbosity: String. Indicates the verbosity of the prints to console.
        :return: Int. Returns the return code of the command
        """
        args = [self.name, source, *self.args]
        if is_verbose(verbosity):
            print(f"Running the following command: \"{' '.join(args)}\"")
        return self._run_subprocess(args, verbosity)

    @classmethod
    def _run_subprocess(cls, args: List[str], verbosity: str) -> int:
        return subprocess.run(  # nosec
            args,
            env=os.environ,
            check=False,
            capture_output=is_silent(verbosity),
        ).returncode
