"""Context class used for reading commands in various contexts."""
from copy import deepcopy
from dataclasses import dataclass, field
from typing import Any, Dict, List, MutableMapping, Optional

from statue.constants import ALIASES, HELP, IS_DEFAULT, PARENT
from statue.exceptions import InvalidStatueConfiguration, UnknownContext


@dataclass
class Context:
    """
    Class representing a command context.

    Commands can be run in different contexts. Contexts allow you to customize the
    command arguments according to the context you are using. For ex
    """

    name: str
    help: str
    aliases: List[str] = field(default_factory=list)
    parent: Optional["Context"] = field(default=None)
    is_default: bool = field(default=False)
    _names: List[str] = field(init=False)

    def __post_init__(self):
        """Extra initialization."""
        self._names = [self.name, *self.aliases]

    def search_context(
        self, setups: MutableMapping[str, Any]
    ) -> Optional[MutableMapping[str, Any]]:
        """
        Search for context in setup dictionary.

        :param setups: Setup to look for the context in
        :type setups: MutableMapping[str, Any]
        :return: Specific setups with context
        :rtype: None or MutableMapping[str, Any]
        """
        for name in self._names:
            name_setups = setups.get(name, None)
            if name_setups is not None:
                return name_setups
        if self.parent is not None:
            return self.parent.search_context(setups)
        if self.is_default:
            return setups
        return None

    @classmethod
    def build_contexts_map(
        cls,
        contexts_config: MutableMapping[str, Any],
        base_contexts_map: Optional[Dict[str, "Context"]] = None,
    ) -> Dict[str, "Context"]:
        """
        Build contexts dictionary from contexts configuration.

        :param contexts_config: Contexts configuration
        :param base_contexts_map: base contexts map to extend, if specifies.
        :type contexts_config: MutableMapping[str, Any]
        :return: Map from context name to context instance:
        :rtype: Dict[str, Context]
        :raises InvalidStatueConfiguration: This exception is raised when trying
            to override a predefined context.
        """
        contexts_map: Dict[str, "Context"] = (
            deepcopy(base_contexts_map) if base_contexts_map is not None else {}
        )
        for name in contexts_config.keys():
            if base_contexts_map is not None and name in base_contexts_map:
                raise InvalidStatueConfiguration(
                    f'"{name}" is a predefined context and cannot be override'
                )
            if name in contexts_map:
                continue
            cls._add_context_to_map(contexts_map, contexts_config, name)
        return contexts_map

    @classmethod
    def _add_context_to_map(
        cls,
        contexts_map: Dict[str, "Context"],
        contexts_config: MutableMapping[str, Any],
        name: str,
    ):
        config = contexts_config.get(name, None)
        if config is None:
            raise UnknownContext(name)
        kwargs = dict(
            name=name, help=config[HELP], is_default=config.get(IS_DEFAULT, False)
        )
        if ALIASES in config:
            kwargs[ALIASES] = config[ALIASES]
        if PARENT in config:
            parent_name = config[PARENT]
            if parent_name not in contexts_map:
                cls._add_context_to_map(contexts_map, contexts_config, parent_name)
            kwargs[PARENT] = contexts_map[parent_name]
        contexts_map[name] = Context(**kwargs)
