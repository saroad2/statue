# noqa: D100
# pylint: disable=missing-module-docstring
import os
import subprocess
from dataclasses import dataclass, field
from typing import Callable, Union


@dataclass(repr=False)
class Command:
    """
    Data class representing a command to run in order to evaluate the code.

    It has the following parameters:
    * name: The name of the command to run
    * args: A callable that gets input paths and return the arguments for the command
    * check_arg: A checking argument that indicates that no formatting actions are
    * help: Help string
     required
    """

    name: str
    args: Callable
    help: str
    check_arg: Union[str, None] = field(default=None)

    def execute(self, input_paths, is_format=False, is_silent=False):
        """
        Execute the command.

        :param is_format: Boolean. Indicates if formatting is required.
        :param is_silent: Boolean. Indicates to run the command without capturing
         output.
        :return: Int. Returns the return code of the command
        """
        args = [self.name, *self.args(input_paths)]
        if not is_format and self.check_arg is not None:
            args.append(self.check_arg)
        return subprocess.run(
            args, env=os.environ, check=False, capture_output=is_silent,
        ).returncode

    def __repr__(self):
        """
        Create a representation string for the command.

        :return: A representation string.
        """
        return f"{self.name} - {self.help}"


COMMANDS = [
    Command(
        name="black",
        args=lambda input_paths: input_paths,
        check_arg="--check",
        help="A code formatter for python",
    ),
    Command(
        name="flake8",
        args=lambda input_paths: [*input_paths, "--max-line-length=88"],
        help="Code style checker for python",
    ),
    Command(
        name="isort",
        args=lambda input_paths: [*input_paths, "--recursive"],
        check_arg="--check-only",
        help="A tool for sorting and cleaning python imports",
    ),
    Command(
        name="pylint", args=lambda input_paths: input_paths, help="Python code linter",
    ),
    Command(
        name="pydocstyle",
        args=lambda input_paths: [*input_paths, "--ignore=D203,D212,D401"],
        help="A tool for python docstring style enforcing",
    ),
]
