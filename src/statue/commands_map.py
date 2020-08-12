"""Commands map allow us to know which commands to run on each source."""
from pathlib import Path
from typing import Optional, List, MutableMapping, Any, Dict, Union

import toml

from statue.command import Command
from statue.commands_reader import read_commands


def get_commands_map(
    sources: List[Union[Path, str]],
    commands_configuration: MutableMapping[str, Any],
    contexts: Optional[List[str]] = None,
    allow_list: Optional[List[str]] = None,
    deny_list: Optional[List[str]] = None,
) -> Optional[Dict[str, List[Command]]]:
    """
    Get commands map from user or from configuration file.

    :param sources: List of sources files specified by the user.
     If empty, get sources from configuration file.
    :param commands_configuration: Commands configuration dictionary,
     used to determine with which arguments to run each command
    :param contexts: List of global contexts.
     Added to the contexts in the configuration file if there are any.
    :param allow_list: List of allowed commands.
     Overriding any commands in the allow_list in the configuration file.
    :param deny_list: List of denied commands.
     Added to the denied commands in the configuration file if there are any.
    :return: Dictionary from source file to the commands to run on it.
    """
    if len(sources) != 0:
        commands = read_commands(
            commands_configuration,
            contexts=contexts,
            allow_list=allow_list,
            deny_list=deny_list,
        )
        return dict.fromkeys([str(source) for source in sources], commands)
    statue_configuration = __get_statue_configuration()
    if statue_configuration is None:
        return None
    commands_map = dict()
    for source, instructions in statue_configuration.items():
        commands_map[str(source)] = read_commands(
            commands_configuration,
            contexts=__combine_if_possible(
                contexts, instructions.get("contexts", None)
            ),
            allow_list=__intersect_if_possible(
                allow_list, instructions.get("allow_list", None)
            ),
            deny_list=__combine_if_possible(
                deny_list, instructions.get("deny_list", None)
            ),
        )
    if len(commands_map) == 0:
        return None
    return commands_map


def __get_statue_configuration():
    statue_configuration_file = Path.cwd() / "statue.toml"
    if not statue_configuration_file.exists():
        return None
    return toml.load(statue_configuration_file)


def __combine_if_possible(list1, list2):
    if list1 is None and list2 is None:
        return None
    list1 = list1 if list1 else []
    list2 = list2 if list2 else []
    return list1 + list2


def __intersect_if_possible(list1, list2):
    if list1 is None:
        return list2
    if list2 is None:
        return list1
    list1 = set(list1) if list1 else set()
    list2 = set(list2) if list2 else set()
    return list(list1.intersection(list2))
