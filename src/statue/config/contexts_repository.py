"""Place for saving all available contexts."""
import itertools
from collections import OrderedDict
from typing import Any, Dict, Iterator, List
from typing import OrderedDict as OrderedDictType

from statue.constants import ALIASES, ALLOWED_BY_DEFAULT, HELP, PARENT
from statue.context import Context
from statue.exceptions import (
    InconsistentConfiguration,
    MissingHelpString,
    UnknownContext,
)


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

    def __contains__(self, item: str) -> bool:
        """
        Does context available in repository.

        :param item: Context name to be searched
        :type item: str
        :return: does context exist in repository
        :rtype: bool
        """
        return item in self.occupied_names

    @property
    def occupied_names(self) -> List[str]:
        """List of all occupied names in contexts repository."""
        occupied_names = list(
            itertools.chain.from_iterable([context.all_names for context in self])
        )
        occupied_names.sort()
        return occupied_names

    def add_contexts(self, *contexts: Context):
        """
        Add contexts to repository.

        :param contexts: Contexts to be added to the repository
        :type contexts: Context
        :raises InconsistentConfiguration: Raised when trying to add contexts with the
            same name or an existing name.
        """
        message = "context name or alias has been defined twice"
        for i, context in enumerate(contexts):
            existing_aliases = [alias for alias in context.all_names if alias in self]
            if len(existing_aliases) != 0:
                raise InconsistentConfiguration(message, location=[existing_aliases[0]])
            for j in range(i):
                other_context = contexts[j]
                overlapping_aliases = [
                    context_alias
                    for context_alias in context.all_names
                    if context_alias in other_context.all_names
                ]
                if len(overlapping_aliases) != 0:
                    raise InconsistentConfiguration(
                        message, location=[overlapping_aliases[0]]
                    )
        self.contexts_list.extend(contexts)

    def remove_context(self, context: Context):
        """
        Remove a context from the repository.

        :param context: Context to be removed from the repository
        :type context: Context
        """
        self.contexts_list.remove(context)

    def reset(self):
        """Clear repository from all contexts."""
        self.contexts_list.clear()

    def as_dict(self) -> OrderedDictType[str, Any]:
        """
        Encode contexts repository as a dictionary.

        This is used in order to serialize the contexts repository in
        a configuration file.

        :return: Serialized representation dictionary
        :rtype: OrderedDict[str, Any]
        """
        contexts_list = list(self)
        contexts_list.sort(key=lambda context: context.name)
        return OrderedDict(
            [(context.name, context.as_dict()) for context in contexts_list]
        )

    @classmethod
    def from_dict(cls, config: Dict[str, Any]) -> "ContextsRepository":
        """
        Create contexts repository from given configuration.

        :param config: Configuration to update repository from
        :type config: Dict[str, Any]
        :return: Contexts repository object.
        :rtype: ContextsRepository
        :raises InconsistentConfiguration: Raised when inconsistency is found in
            configuration.
        """
        contexts_repository = ContextsRepository()
        context_names = set(config.keys())
        while len(context_names) != 0:
            available_contexts = [
                context_name
                for context_name in context_names
                if cls._can_be_built(
                    context_config=config[context_name],
                    contexts_repository=contexts_repository,
                )
            ]
            if len(available_contexts) == 0:
                raise InconsistentConfiguration(
                    "The following contexts cannot be built because they are missing "
                    "or they cause circular parenting: "
                    f"{', '.join(context_names)}"
                )
            for context_name in available_contexts:
                context_names.remove(context_name)
                cls._add_context_from_config(
                    context_name=context_name,
                    context_config=config[context_name],
                    contexts_repository=contexts_repository,
                )
        return contexts_repository

    @classmethod
    def _add_context_from_config(
        cls,
        context_name: str,
        context_config: Dict[str, Any],
        contexts_repository: "ContextsRepository",
    ):
        """
        Add context from given configuration to contexts repository.

        If context is not available in configuration, try get it
        from the repository (if it exists).

        :param context_name: Context to be built
        :type context_name: str
        :param context_config: Configuration to build context from
        :type context_config: Dict[str, Any]
        :param contexts_repository: Contexts repository to add new context to
        :type contexts_repository: ContextsRepository
        :raises MissingHelpString: Raised when help string is missing
        """
        parent = (
            contexts_repository[context_config[PARENT]]
            if PARENT in context_config
            else None
        )
        aliases = context_config.get(ALIASES, [])
        if HELP not in context_config:
            raise MissingHelpString(location=[context_name])
        contexts_repository.add_contexts(
            Context(
                name=context_name,
                help=context_config[HELP],
                aliases=aliases,
                parent=parent,
                allowed_by_default=context_config.get(ALLOWED_BY_DEFAULT, False),
            )
        )

    @classmethod
    def _can_be_built(
        cls, context_config: Dict[str, Any], contexts_repository: "ContextsRepository"
    ) -> bool:
        if PARENT not in context_config:
            return True
        if context_config[PARENT] in contexts_repository:
            return True
        return False
