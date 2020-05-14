from pathlib import Path
from typing import Union

import toml

from eddington_static.command import Command


def read_commands(path: Union[str, Path], is_test=False, is_format=False):
    if not isinstance(path, Path):
        path = Path(path)
    config = toml.load(path)
    commands = []
    for command, setups in config.items():
        commands.append(
            Command(
                name=command,
                args=__read_args(setups, is_test=is_test, is_format=is_format),
                help=setups["help"],
                fast=setups.get("fast", False),
            )
        )
    return commands


def __read_args(setups: dict, is_test=False, is_format=False):
    if is_test and "test" in setups:
        return setups["test"].get("args", [])
    if is_format and "format" in setups:
        return setups["format"].get("args", [])
    return setups.get("args", [])
