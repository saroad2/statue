from dataclasses import dataclass, field
from typing import Any, Dict, List, MutableMapping, Optional

from statue.constants import ALIASES, HELP, IS_DEFAULT, PARENT
from statue.exceptions import UnknownContext


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
        self._names = [self.name, *self.aliases]

    def search_context(self, setups):
        for name in self._names:
            name_setups = setups.get(name, None)
            if name_setups is not None:
                return name_setups
        if self.parent is not None:
            return self.parent.search_context(setups)
        if self.is_default:
            return True
        return None

    @classmethod
    def build_contexts_map(cls, contexts_config: MutableMapping[str, Any]):
        contexts_map = {}
        for name in contexts_config.keys():
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
