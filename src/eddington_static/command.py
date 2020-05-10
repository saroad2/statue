# noqa: D100
# pylint: disable=missing-module-docstring
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
