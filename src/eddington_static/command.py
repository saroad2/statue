from dataclasses import dataclass, field
from typing import List, Union


@dataclass
class Command:

    name: str
    args: List[str]
    check_arg: Union[str, None] = field(default=None)
