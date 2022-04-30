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

    @classmethod
    def validate(  # pylint: disable=too-many-arguments
        cls,
        command_name: str,
        args: Optional[List[str]],
        add_args: Optional[List[str]],
        clear_args: bool,
        context_name: str,
    ):
        """
        Validate that the context specification does contradict itself.

        :param command_name: Name of the command of the builder
        :type command_name: str
        :param args: Optional arguments for the context specification
        :type args: Optional[List[str]]
        :param add_args: Optional added arguments for the context specification
        :type add_args: Optional[List[str]]
        :param clear_args: boolean stating if arguments are cleared
        :type clear_args: bool
        :param context_name: Name of the context for the context specification
        :type context_name: str
        :raises InconsistentConfiguration: raised when context
            specification is inconsistent.
        """
        if clear_args and args is not None:
            raise InconsistentConfiguration(
                "args and clear_args cannot be both set at the same time",
                location=[command_name, context_name, "args/clear_args"],
            )

        if clear_args and add_args is not None:
            raise InconsistentConfiguration(
                "add_args and clear_args cannot be both set at the same time",
                location=[command_name, context_name, "add_args/clear_args"],
            )

        if args is not None and add_args is not None:
            raise InconsistentConfiguration(
                "args and add_args cannot be both set at the same time",
                location=[command_name, context_name, "args/add_args"],
            )

    @classmethod
    def from_dict(
        cls,
        command_name: str,
        context_specification_setups: Dict[str, Any],
        context_name: str,
    ) -> "ContextSpecification":
        """
        Read Context specification from json.

        :param command_name: Name of the command to be built
        :type command_name: str
        :param context_specification_setups: Context specification json
        :type context_specification_setups: Dict[str, Any]
        :param context_name: context name
        :type context_name: str
        :return: Built context specification
        :rtype: ContextSpecification
        """
        args = context_specification_setups.get(ARGS, None)
        add_args = context_specification_setups.get(ADD_ARGS, None)
        clear_args = context_specification_setups.get(CLEAR_ARGS, False)

        cls.validate(
            command_name=command_name,
            args=args,
            add_args=add_args,
            clear_args=clear_args,
            context_name=context_name,
        )
        return ContextSpecification(args=args, add_args=add_args, clear_args=clear_args)
