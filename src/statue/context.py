"""Context class used for reading commands in various contexts."""
from collections import OrderedDict
from dataclasses import dataclass, field
from typing import Any, List, MutableMapping, Optional

from statue.constants import ALIASES, ALLOWED_BY_DEFAULT, HELP, PARENT


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

    def __hash__(self) -> int:
        """
        Hash context according to its name.

        :return: hash
        :rtype: int
        """
        return hash(self.name)

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

    def as_dict(self) -> OrderedDict[str, Any]:
        """
        Encode context as a dictionary.

        This is used in order to serialize the context in a configuration file.

        :return: Serialized representation dictionary
        :rtype: OrderedDict[str, Any]
        """
        context_dict: OrderedDict[str, Any] = OrderedDict()
        context_dict[HELP] = self.help
        if len(self.aliases) != 0:
            context_dict[ALIASES] = self.aliases
        if self.parent is not None:
            context_dict[PARENT] = self.parent.name
        if self.allowed_by_default:
            context_dict[ALLOWED_BY_DEFAULT] = True
        return context_dict
