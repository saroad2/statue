"""Context class used for reading commands in various contexts."""
from copy import deepcopy
from dataclasses import dataclass, field
from typing import Any, Dict, List, MutableMapping, Optional

from statue.constants import (
    ALIASES,
    ALLOWED_BY_DEFAULT,
    ALLOWED_CONTEXTS,
    HELP,
    PARENT,
    REQUIRED_CONTEXTS,
)
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
    allowed_by_default: bool = field(default=False)

    @property
    def all_names(self) -> List[str]:
        """List of all possible names."""
        return [self.name, *self.aliases]

    def is_matching(self, name: str) -> bool:
        """
        Check if a given name is identical to one of the contexts names.

        :param name: Name to be checked
        :type name: str
        :return: Is name equal to context name or one of its aliases
        :rtype: bool
        """
        return name in self.all_names

    def is_matching_recursively(self, name: str) -> bool:
        """
        Check if given name matches this context or its parent.

        :param name: Name to be checked
        :type name: str
        :return: Is name matching to this context or its parent.
        :rtype: bool
        """
        if self.is_matching(name):
            return True
        if self.parent is not None:
            return self.parent.is_matching_recursively(name)
        return False

    def is_allowed(self, setups: MutableMapping[str, Any]) -> bool:
        """
        Check if this command is allowed in the given setup.

        :param setups: Setup to check if the context is allowed in
        :type setups: MutableMapping[str, Any]
        :return: Is this context allowed or not
        :rtype: bool
        """
        names_to_check = list(setups.keys())
        names_to_check.extend(setups.get(REQUIRED_CONTEXTS, []))
        names_to_check.extend(setups.get(ALLOWED_CONTEXTS, []))
        if any(self.is_matching_recursively(name) for name in names_to_check):
            return True
        return self.allowed_by_default

    def search_context_instructions(
        self, setups: MutableMapping[str, Any]
    ) -> Optional[MutableMapping[str, Any]]:
        """
        Search for context in setup dictionary.

        :param setups: Setup to look for the context in
        :type setups: MutableMapping[str, Any]
        :return: Specific setups with context
        :rtype: None or MutableMapping[str, Any]
        """
        for name in self.all_names:
            name_setups = setups.get(name, None)
            if name_setups is not None:
                return name_setups
        if self.parent is not None:
            return self.parent.search_context_instructions(setups)
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
            name=name,
            help=config[HELP],
            allowed_by_default=config.get(ALLOWED_BY_DEFAULT, False),
        )
        if ALIASES in config:
            kwargs[ALIASES] = config[ALIASES]
        if PARENT in config:
            parent_name = config[PARENT]
            if parent_name not in contexts_map:
                cls._add_context_to_map(contexts_map, contexts_config, parent_name)
            kwargs[PARENT] = contexts_map[parent_name]
        contexts_map[name] = Context(**kwargs)
