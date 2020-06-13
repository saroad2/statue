"""Reader method for settings."""
from pathlib import Path
from typing import List, Union

import toml

from statue.command import Command
from statue.constants import HELP, ARGS, STANDARD, CLEAR_ARGS, ADD_ARGS


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
                help=setups[HELP],
            )
        )
    return commands


def __skip_command(setups: dict, filters: List[str]):
    if len(filters) == 0:
        return not setups.get(STANDARD, True)
    for command_filter in filters:
        if not setups.get(command_filter, False):
            return True
    return False


def __read_args(setups: dict, filters: List[str]):
    base_args = setups.get(ARGS, [])
    for command_filter in filters:
        filter_obj = setups.get(command_filter, None)
        if not isinstance(filter_obj, dict):
            continue
        args = filter_obj.get(ARGS, None)
        if args is not None:
            return args
        add_args = filter_obj.get(ADD_ARGS, None)
        if add_args is not None:
            base_args.extend(add_args)
        clear_args = filter_obj.get(CLEAR_ARGS, False)
        if clear_args:
            return []
    return base_args
