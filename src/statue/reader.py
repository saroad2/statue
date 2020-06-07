"""Reader method for settings."""
from pathlib import Path
from typing import List, Union

import toml

from statue.command import Command


def read_commands(path: Union[str, Path], filters: List[str] = None):
    """
    Read commands from a settings file.

    :param path: Path. the path of the settings file
    :param filters: List of str. a list of filters to choose commands from.
    :return: a list of :class:`Command`
    """
    if not isinstance(path, Path):
        path = Path(path)
    config = toml.load(path)
    commands = []
    filters = [] if filters is None else filters
    for command, setups in config.items():
        if __skip_command(setups, filters):
            continue
        commands.append(
            Command(
                name=command,
                args=__read_args(setups, filters=filters),
                help=setups["help"],
            )
        )
    return commands


def __skip_command(setups: dict, filters: List[str]):
    if len(filters) == 0:
        return not setups.get("standard", True)
    for command_filter in filters:
        if not setups.get(command_filter, False):
            return True
    return False


def __read_args(setups: dict, filters: List[str]):
    for command_filter in filters:
        filter_obj = setups.get(command_filter, None)
        if not isinstance(filter_obj, dict):
            continue
        args = filter_obj.get("args", None)
        if args is not None:
            return args
    return setups.get("args", [])
