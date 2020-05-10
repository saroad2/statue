# noqa: D100
# pylint: disable=missing-module-docstring
import os
import subprocess
from dataclasses import dataclass, field
from typing import List, Union


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

    def execute(self, is_format=False):
        """
        Execute the command.

        :param is_format: Boolean. Indicates if formatting is required.
        :return: Int. Returns the return code of the command
        """
        args = [self.name, *self.args]
        if not is_format and self.check_arg is not None:
            args.append(self.check_arg)
        return subprocess.run(args, env=os.environ, check=False).returncode
