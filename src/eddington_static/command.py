# noqa: D100
# pylint: disable=missing-module-docstring
import os
import subprocess
from dataclasses import dataclass, field
from typing import List, Union

from eddington_static.constants import RESOURCES_PATH


@dataclass
class Command:
    """
    Data class representing a command to run in order to evaluate the code.

    It has 3 variables:
    * name: The name of the command to run
    * args: The arguments of the command
    * check_arg: A checking argument that indicates that no formatting actions are
     required
    """

    name: str
    args: List[str]
    check_arg: Union[str, None] = field(default=None)

    def execute(self, is_format=False, is_silent=False):
        """
        Execute the command.

        :param is_format: Boolean. Indicates if formatting is required.
        :param is_silent: Boolean. Indicates to run the command without capturing
         output.
        :return: Int. Returns the return code of the command
        """
        args = [self.name, *self.args]
        if not is_format and self.check_arg is not None:
            args.append(self.check_arg)
        return subprocess.run(
            args, env=os.environ, check=False, capture_output=is_silent,
        ).returncode


def create_commands(input_paths):
    """
    Create list of commands to perform on input path.

    :param input_paths: List of strings. Path to perform static code anlysis on.
    :return: List of :ref:`Command` objects.
    """
    return [
        Command(name="black", args=input_paths, check_arg="--check"),
        Command(
            name="flake8", args=[*input_paths, f"--config={RESOURCES_PATH / '.flake8'}"]
        ),
        Command(
            name="isort",
            args=[
                *input_paths,
                "--recursive",
                f"--settings-path={RESOURCES_PATH / '.isort.cfg'}",
            ],
            check_arg="--check-only",
        ),
        Command(name="pylint", args=input_paths),
        Command(
            name="pydocstyle",
            args=[*input_paths, f"--config={RESOURCES_PATH / '.pydocstyle.ini'}"],
        ),
    ]
