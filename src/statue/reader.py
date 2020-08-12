"""Reader method for settings."""
from pathlib import Path
from typing import List, Union, Optional

import toml

from statue.command import Command
from statue.constants import HELP, ARGS, STANDARD, CLEAR_ARGS, ADD_ARGS


def read_commands(
    path: Union[str, Path],
    contexts: Optional[List[str]] = None,
    allow_list: Optional[List[str]] = None,
    deny_list: Optional[List[str]] = None,
):
    """
    Read commands from a settings file.

    :param path: Path. the path of the settings file
    :param contexts: List of str. a list of contexts to choose commands from.
    :param allow_list: List of allowed commands. If None, take all commands
    :param deny_list: List of denied commands. If None, take all commands
    :return: a list of :class:`Command`
    """
    if not isinstance(path, Path):
        path = Path(path)
    config = toml.load(path)
    commands = []
    contexts = [] if contexts is None else contexts
    for command_name, setups in config.items():
        if __skip_command(command_name, setups, contexts, allow_list, deny_list):
            continue
        commands.append(
            Command(
                name=command_name,
                args=__read_args(setups, contexts=contexts),
                help=setups[HELP],
            )
        )
    return commands


def __skip_command(
    commands_name: str,
    setups: dict,
    contexts: List[str],
    allow_list: Optional[List[str]],
    deny_list: Optional[List[str]],
):
    if allow_list is not None and commands_name not in allow_list:
        return True
    if deny_list is not None and commands_name in deny_list:
        return True
    if len(contexts) == 0:
        return not setups.get(STANDARD, True)
    for command_context in contexts:
        if not setups.get(command_context, False):
            return True
    return False


def __read_args(setups: dict, contexts: List[str]):
    base_args = setups.get(ARGS, [])
    for command_context in contexts:
        context_obj = setups.get(command_context, None)
        if not isinstance(context_obj, dict):
            continue
        args = context_obj.get(ARGS, None)
        if args is not None:
            return args
        add_args = context_obj.get(ADD_ARGS, None)
        if add_args is not None:
            base_args.extend(add_args)
        clear_args = context_obj.get(CLEAR_ARGS, False)
        if clear_args:
            return []
    return base_args
