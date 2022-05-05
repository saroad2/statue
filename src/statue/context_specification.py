"""Specific arguments manipulations for given context."""
from collections import OrderedDict
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from typing import OrderedDict as OrderedDictType

from statue.constants import ADD_ARGS, ARGS, CLEAR_ARGS
from statue.exceptions import InconsistentConfiguration


@dataclass
class ContextSpecification:
    """Specific instructions for building command in context."""

    args: Optional[List[str]] = field(default=None)
    add_args: Optional[List[str]] = field(default=None)
    clear_args: bool = field(default=False)

    def __post_init__(self):
        """Validate after initializing."""
        self._validate()

    def update_args(self, args: List[str]) -> List[str]:
        """
        Update command arguments according to instructions.

        :param args: Original arguments
        :type args: List[str]
        :return: Updated arguments
        :rtype: List[str]
        """
        if self.args is not None:
            return self.args
        if self.add_args is not None:
            return args + self.add_args
        if self.clear_args:
            return []
        return args

    def as_dict(self) -> OrderedDictType[str, Any]:
        """
        Encode context specification as a dictionary.

        This is used in order to serialize the context specification in
        a configuration file.

        :return: Serialized representation dictionary
        :rtype: OrderedDict[str, Any]
        """
        specification_as_dict: OrderedDictType[str, Any] = OrderedDict()
        if self.args is not None:
            specification_as_dict[ARGS] = self.args
        if self.add_args is not None:
            specification_as_dict[ADD_ARGS] = self.add_args
        if self.clear_args:
            specification_as_dict[CLEAR_ARGS] = True
        return specification_as_dict

    def _validate(self):
        """
        Validate that the context specification does contradict itself.

        :raises InconsistentConfiguration: raised when context
            specification is inconsistent.
        """
        if self.clear_args and self.args is not None:
            raise InconsistentConfiguration(
                "args and clear_args cannot be both set at the same time",
                location=["args/clear_args"],
            )

        if self.clear_args and self.add_args is not None:
            raise InconsistentConfiguration(
                "add_args and clear_args cannot be both set at the same time",
                location=["add_args/clear_args"],
            )

        if self.args is not None and self.add_args is not None:
            raise InconsistentConfiguration(
                "args and add_args cannot be both set at the same time",
                location=["args/add_args"],
            )

    @classmethod
    def from_dict(
        cls, context_specification_setups: Dict[str, Any]
    ) -> "ContextSpecification":
        """
        Read Context specification from json.

        :param context_specification_setups: Context specification json
        :type context_specification_setups: Dict[str, Any]
        :return: Built context specification
        :rtype: ContextSpecification
        """
        return ContextSpecification(
            args=context_specification_setups.get(ARGS, None),
            add_args=context_specification_setups.get(ADD_ARGS, None),
            clear_args=context_specification_setups.get(CLEAR_ARGS, False),
        )
