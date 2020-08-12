# noqa: D100
# pylint: disable=missing-module-docstring
import os
import subprocess
from dataclasses import dataclass, field
from typing import List


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

    def execute(  # pylint: disable=too-many-arguments
        self, source: str, is_silent: bool = False, is_verbose: bool = False,
    ) -> int:
        """
        Execute the command.

        :param source: source files to check.
        :param is_silent: Boolean. Indicates to run the command without capturing
         output.
        :param is_verbose: Boolean. Run commands verbosely
        :return: Int. Returns the return code of the command
        """
        args = [self.name, source, *self.args]
        if is_verbose:
            print(f"Running the following command: \"{' '.join(args)}\"")
        return subprocess.run(
            args, env=os.environ, check=False, capture_output=is_silent,
        ).returncode
