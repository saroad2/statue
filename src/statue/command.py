# noqa: D100
# pylint: disable=missing-module-docstring
import os
import subprocess
from dataclasses import dataclass, field
from typing import List, Union


@dataclass(repr=False)
class Command:
    """
    Data class representing a command to run in order to evaluate the code.

    :param name: The name of the command to run.
    :param args: A list of arguments for the command.
    :param help: Help string
    """

    name: str
    help: str
    args: Union[List[str], None] = field(default=None)

    def execute(  # pylint: disable=too-many-arguments
        self, input_paths: List[str], is_silent: bool = False, is_verbose: bool = False,
    ) -> int:
        """
        Execute the command.

        :param input_paths: input files to check.
        :param is_silent: Boolean. Indicates to run the command without capturing
         output.
        :param is_verbose: Boolean. Run commands verbosely
        :return: Int. Returns the return code of the command
        """
        args = [self.name, *input_paths]
        if self.args is not None:
            args.extend(self.args)
        if is_verbose:
            print(f"Running the following command: \"{' '.join(args)}\"")
        return subprocess.run(
            args, env=os.environ, check=False, capture_output=is_silent,
        ).returncode
