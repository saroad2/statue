"""Context class used for reading commands in various contexts."""
from collections import OrderedDict
from typing import Any, Dict, Iterable, List, Optional
from typing import OrderedDict as OrderedDictType

from statue.constants import ALIASES, ALLOWED_BY_DEFAULT, HELP, PARENT
from statue.exceptions import ContextCircularParentingError


class Context:
    """
    Class representing a command context.

    Commands can be run in different contexts. Contexts allow you to customize the
    command arguments according to the context you are using. For ex
    """

    def __init__(  # pylint: disable=too-many-arguments
        self,
        name: str,
        help: str,  # pylint: disable=redefined-builtin
        aliases: Optional[Iterable[str]] = None,
        parent: Optional["Context"] = None,
        allowed_by_default: bool = False,
    ):
        """
        Context constructor.

        :param name: Name of the context
        :type name: str
        :param help: Short help string to describe context
        :type help: str
        :param aliases: List of possible aliases of the context
        :type aliases: Optional[Iterable[str]]
        :param parent: Optional parent context for this context
        :type parent: Optional[Context]
        :param allowed_by_default: Allow this context for all commands by default
        :type allowed_by_default: bool
        """
        self.name = name
        self.help = help
        self.aliases = list(aliases) if aliases is not None else []
        self.parent = parent
        self.allowed_by_default = allowed_by_default

    @property
    def parent(self) -> Optional["Context"]:
        """Get parent of this context."""
        return self._parent

    @parent.setter
    def parent(self, parent: Optional["Context"]):
        """
        Set parent of this context.

        :param parent: Desired parent
        :type parent: Context
        :raises ContextCircularParentingError: Raised when trying to set a parent
            which is a child of this context.
        """
        if parent is not None and parent.is_child_of(self):
            raise ContextCircularParentingError(self.name, parent.name)
        self._parent = parent

    @property
    def parents(self) -> List["Context"]:
        """Get all parents recursively for this context."""
        if self.parent is None:
            return []
        return [self.parent, *self.parent.parents]

    def __eq__(self, other: object) -> bool:
        """
        Check equality between two contexts.

        :param other: other object to compare to
        :type other: object
        :return: are contexts equal
        :rtype: bool
        """
        return (
            isinstance(other, Context)
            and self.name == other.name
            and self.help == other.help
            and self.aliases == other.aliases
            and self.parent == other.parent
            and self.allowed_by_default == other.allowed_by_default
        )

    def __repr__(self) -> str:
        """
        String representation of the context.

        :return: context as string
        :rtype: str
        """
        return (
            "Context("
            f"name='{self.name}', "
            f"help='{self.help}', "
            f"aliases={self.aliases}, "
            f"parent={self.parent}, "
            f"allowed_by_default={self.allowed_by_default}"
            ")"
        )

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

    def clear_aliases(self):
        """Remove all aliases of context."""
        self.aliases.clear()

    def is_child_of(self, parent: "Context") -> bool:
        """
        Checks if this context is a child of another context.

        :param parent: Possible parent for this context.
        :type parent: Context
        :return: Is this context child of the given context
        :rtype: bool
        """
        if self.parent == parent:
            return True
        if self.parent is None:
            return False
        return self.parent.is_child_of(parent)

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
        for parent in self.parents:
            if parent.is_matching(name):
                return True
        return False

    def search_context_instructions(
        self, setups: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Search for context in setup dictionary.

        :param setups: Setup to look for the context in
        :type setups: Dict[str, Any]
        :return: Specific setups with context
        :rtype: None or Dict[str, Any]
        """
        for name in self.all_names:
            name_setups = setups.get(name, None)
            if name_setups is not None:
                return name_setups
        for parent in self.parents:
            instructions = parent.search_context_instructions(setups)
            if instructions is not None:
                return instructions
        return None

    def as_dict(self) -> OrderedDictType[str, Any]:
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
