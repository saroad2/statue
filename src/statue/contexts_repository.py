from typing import Any, MutableMapping

from statue.constants import ALIASES, PARENT
from statue.context import Context
from statue.exceptions import InconsistentConfiguration, UnknownContext


class ContextsRepository:
    def __init__(self, *contexts: Context):
        self.contexts_list = list(contexts)

    @property
    def contexts_number(self):
        return len(self.contexts_list)

    def __iter__(self):
        return iter(self.contexts_list)

    def add_contexts(self, *contexts: Context):
        self.contexts_list.extend(contexts)

    def get_context(self, context_name: str) -> Context:
        for context in self.contexts_list:
            if context.is_matching(context_name):
                return context
        raise UnknownContext(context_name=context_name)

    def has_context(self, context_name: str) -> bool:
        try:
            self.get_context(context_name)
        except UnknownContext:
            return False
        return True

    def reset(self):
        self.contexts_list.clear()

    def update_from_config(self, config: MutableMapping[str, Any]):
        context_names = set(config.keys())
        while len(context_names) != 0:
            context_name = context_names.pop()
            if self.has_context(context_name):
                raise InconsistentConfiguration(
                    f'"{context_name}" is a already defined context and '
                    "cannot defined twice"
                )
            self.contexts_list.append(
                self.build_context_from_config(context_name, config)
            )

    def build_context_from_config(
        self, context_name: str, config: MutableMapping[str, Any]
    ) -> Context:
        if context_name not in config:
            return self.get_context(context_name)
        context_config = dict(config[context_name])
        if PARENT in context_config:
            context_config[PARENT] = self.build_context_from_config(
                context_config[PARENT], config
            )
        if ALIASES in context_config:
            for alias in context_config[ALIASES]:
                if not self.has_context(alias):
                    continue
                raise InconsistentConfiguration(
                    f'"{alias}" cannot be defined as an alias for "{context_name}" '
                    "because a context is already defined with this name"
                )
        return Context(name=context_name, **context_config)
