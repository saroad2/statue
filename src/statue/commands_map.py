"""Commands map allow us to know which commands to run on each source."""
from pathlib import Path
from typing import Any, Dict, List, MutableMapping, Optional, Set, Union

from statue.command import Command
from statue.commands_reader import read_commands
from statue.constants import ALLOW_LIST, COMMANDS, CONTEXTS, DENY_LIST, SOURCES


def get_commands_map(
    sources: List[Union[Path, str]],
    statue_configuration: MutableMapping[str, Any],
    contexts: Optional[List[str]] = None,
    allow_list: Optional[List[str]] = None,
    deny_list: Optional[List[str]] = None,
) -> Optional[Dict[str, List[Command]]]:
    """
    Get commands map from user or from configuration file.

    :param sources: List of sources files specified by the user.
     If empty, get sources from configuration file.
    :param statue_configuration: Statue configuration dictionary,
     used to determine with which arguments to run each command
    :param contexts: List of global contexts.
     Added to the contexts in the configuration file if there are any.
    :param allow_list: List of allowed commands.
     Overriding any commands in the allow_list in the configuration file.
    :param deny_list: List of denied commands.
     Added to the denied commands in the configuration file if there are any.
    :return: Dictionary from source file to the commands to run on it.
    """
    commands_configuration = statue_configuration[COMMANDS]
    if len(sources) != 0:
        commands = read_commands(
            commands_configuration,
            contexts=contexts,
            allow_list=allow_list,
            deny_list=deny_list,
        )
        return dict.fromkeys([str(source) for source in sources], commands)
    commands_map = dict()
    for source, instructions in statue_configuration.get(SOURCES, {}).items():
        commands = read_commands(
            commands_configuration,
            contexts=__combine_if_possible(contexts, instructions.get(CONTEXTS, None)),
            allow_list=__intersect_if_possible(
                allow_list, instructions.get(ALLOW_LIST, None)
            ),
            deny_list=__combine_if_possible(
                deny_list, instructions.get(DENY_LIST, None)
            ),
        )
        if len(commands) != 0:
            commands_map[str(source)] = commands
    if len(commands_map) == 0:
        return None
    return commands_map


def __combine_if_possible(
    list1: Optional[List[str]], list2: Optional[List[str]]
) -> Optional[List[str]]:
    if list1 is None and list2 is None:
        return None
    list1 = list(list1) if list1 else []
    list2 = list(list2) if list2 else []
    return list1 + list2


def __intersect_if_possible(
    list1: Optional[List[str]], list2: Optional[List[str]]
) -> Optional[List[str]]:
    if list1 is None:
        return list2
    if list2 is None:
        return list1
    set1: Set[str] = set(list1) if list1 else set()
    set2: Set[str] = set(list2) if list2 else set()
    return list(set1.intersection(set2))
