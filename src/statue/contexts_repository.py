"""Place for saving all available contexts."""
from typing import Any, Iterator, MutableMapping

from statue.constants import ALIASES, PARENT
from statue.context import Context
from statue.exceptions import InconsistentConfiguration, UnknownContext


class ContextsRepository:
    """Repository class for saving and accessing contexts."""

    def __init__(self, *contexts: Context):
        """
        Constructor.

        :param contexts: Initial contexts to be saved
        :type contexts: Context
        """
        self.contexts_list = list(contexts)

    def __len__(self) -> int:
        """
        Number of available contexts.

        :return: Number of contexts
        :rtype: int
        """
        return len(self.contexts_list)

    def __iter__(self) -> Iterator[Context]:
        """
        Iterate over all available contexts.

        :return: Contexts iterator
        :rtype: Iterator[Context]
        """
        return iter(self.contexts_list)

    def __getitem__(self, item: str) -> Context:
        """
        Get context by name or alias.

        :param item: Context name or alias to be retrieved
        :type item: str
        :return: Context with given name
        :rtype: Context
        :raises UnknownContext: Raised when context is not found
        """
        for context in self.contexts_list:
            if context.is_matching(item):
                return context
        raise UnknownContext(context_name=item)

    def add_contexts(self, *contexts: Context):
        """
        Add contexts to repository.

        :param contexts: Contexts to be added to the repository
        :type contexts: Context
        """
        self.contexts_list.extend(contexts)

    def has_context(self, context_name: str) -> bool:
        """
        Does context available in repository.

        :param context_name: Context name to be searched
        :type context_name: str
        :return: does context exist in repository
        :rtype: bool
        """
        try:
            self[context_name]
        except UnknownContext:
            return False
        return True

    def reset(self):
        """Clear repository from all contexts."""
        self.contexts_list.clear()

    def update_from_config(self, config: MutableMapping[str, Any]):
        """
        Update contexts repository from given configuration.

        :param config: Configuration to update repository from
        :type config: MutableMapping[str, Any]
        :raises InconsistentConfiguration: Raised when inconsistency is found in
            configuration.
        """
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
        """
        Build context from given configuration.

        If context is not available in configuration, try get it
        from the repository (if it exists).

        :param context_name: Context to be built
        :type context_name: str
        :param config: Configuration to build context from
        :type config: MutableMapping[str, Any]
        :return: Built context.
        :rtype: Context
        :raises InconsistentConfiguration: Raised when inconsistency is found in
            configuration.
        """
        if context_name not in config:
            return self[context_name]
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
