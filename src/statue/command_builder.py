"""Build commands from configuration."""
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from statue.command import Command
from statue.constants import (
    ADD_ARGS,
    ALLOWED_CONTEXTS,
    ARGS,
    CLEAR_ARGS,
    HELP,
    REQUIRED_CONTEXTS,
    VERSION,
)
from statue.context import Context
from statue.exceptions import InconsistentConfiguration, InvalidCommand


@dataclass
class ContextSpecification:
    """Specific instructions for building command in context."""

    args: Optional[List[str]] = field(default=None)
    add_args: Optional[list[str]] = field(default=None)
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

    @classmethod
    def validate(  # pylint: disable=too-many-arguments
        cls,
        command_name: str,
        args: Optional[List[str]],
        add_args: Optional[List[str]],
        clear_args: bool,
        context_name: Optional[str] = None,
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
        :type context_name: Optional[str]
        :raises InconsistentConfiguration: raised when context
            specification is inconsistent.
        """
        error_prefix = f"Inconsistency in {command_name}"
        if context_name is not None:
            error_prefix += f" context specification for {context_name}"
        error_prefix += ":"
        error_suffix = "cannot be both set at the same time"

        if clear_args and args is not None:
            raise InconsistentConfiguration(
                f"{error_prefix} clear_args and args {error_suffix}"
            )

        if clear_args and add_args is not None:
            raise InconsistentConfiguration(
                f"{error_prefix} clear_args and add_args {error_suffix}"
            )

        if args is not None and add_args is not None:
            raise InconsistentConfiguration(
                f"{error_prefix} args and add_args {error_suffix}"
            )

    @classmethod
    def from_json(
        cls,
        command_name: str,
        context_specification_setups: Dict[str, Any],
        context_name: Optional[str] = None,
    ) -> "ContextSpecification":
        """
        Read Context specification from json.

        :param command_name: Name of the command to be built
        :type command_name: str
        :param context_specification_setups: Context specification json
        :type context_specification_setups: Dict[str, Any]
        :param context_name: Optional context name
        :type context_name: Optional[str]
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

    @classmethod
    def configuration_keys(cls) -> List[str]:
        """
        All keys used for configuration.

        :return: Configuration keys
        :rtype: List[str]
        """
        return [ARGS, ADD_ARGS, CLEAR_ARGS]


@dataclass
class CommandBuilder:  # pylint: disable=too-many-instance-attributes
    """Command builder as specified in configuration."""

    name: str
    help: str
    default_args: List[str] = field(default_factory=list)
    version: Optional[str] = field(default=None)
    required_contexts: List[str] = field(default_factory=list)
    allowed_contexts: List[str] = field(default_factory=list)
    contexts_specifications: Dict[str, ContextSpecification] = field(
        default_factory=dict
    )

    @property
    def available_contexts(self) -> List[str]:
        """Contexts which are available to use according to this command."""
        return [
            *self.required_contexts,
            *self.allowed_contexts,
            *self.contexts_specifications.keys(),
        ]

    def build_command(self, *contexts: Context) -> Command:
        """
        Build command according to given contexts.

        :param contexts: Specified contexts to build command according to.
        :type contexts: Context
        :return: Built command.
        :rtype: Command
        :raises InvalidCommand: Raised when given contexts doesn't match
            the command's requirements
        """
        missing_required_contexts = [
            required_context
            for required_context in self.required_contexts
            if all(
                not context.is_matching_recursively(required_context)
                for context in contexts
            )
        ]
        if len(missing_required_contexts) != 0:
            raise InvalidCommand(
                f"Command `{self.name}`"
                "requires the following contexts, which are missing: "
                f"{', '.join(missing_required_contexts)}"
            )
        not_allowed_contexts = [
            context.name
            for context in contexts
            if all(
                not context.is_matching_recursively(available_context)
                for available_context in self.available_contexts
            )
        ]
        if len(not_allowed_contexts) != 0:
            raise InvalidCommand(
                f"Command `{self.name}`"
                "is not allowed due to the following contexts: "
                f"{', '.join(not_allowed_contexts)}"
            )
        return Command(
            name=self.name,
            help=self.help,
            args=self.build_args(*contexts),
            version=self.version,
        )

    def build_args(self, *contexts: Context) -> List[str]:
        """
        Build arguments for command according to contexts.

        :param contexts: Specified contexts to arguments
            command according to.
        :type contexts: Context
        :return: Arguments list
        :rtype: List[str]
        """
        args = list(self.default_args)
        for context in contexts:
            args = self.get_context_specification(context).update_args(args)
        return args

    def get_context_specification(self, context: Context) -> ContextSpecification:
        """
        Get context specification from context name.

        :param context: Specified context
        :type context: Context
        :return: Context specification to build command according to
        :rtype: ContextSpecification
        """
        for context_name, context_specification in self.contexts_specifications.items():
            if context.is_matching_recursively(context_name):
                return context_specification
        return ContextSpecification()

    def update_from_config(self, builder_setups: Dict[str, Any]):
        """
        Update command builder according to a given configuration.

        :param builder_setups: Command builder configuration
        :type builder_setups: Dict[str, Any]
        """
        # Copy in order to avoid configuration contamination
        builder_setups = dict(builder_setups)

        self.default_args = ContextSpecification.from_json(
            command_name=self.name, context_specification_setups=builder_setups
        ).update_args(self.default_args)

        for key in ContextSpecification.configuration_keys():
            builder_setups.pop(key, None)
        self.version = builder_setups.pop(VERSION, self.version)
        self.required_contexts.extend(builder_setups.pop(REQUIRED_CONTEXTS, []))
        self.allowed_contexts.extend(builder_setups.pop(ALLOWED_CONTEXTS, []))
        self.contexts_specifications.update(
            {
                context_name: ContextSpecification.from_json(
                    command_name=self.name,
                    context_name=context_name,
                    context_specification_setups=context_specification,
                )
                for context_name, context_specification in builder_setups.items()
            }
        )

    @classmethod
    def from_json(cls, command_name, builder_setups: Dict[str, Any]):
        """
        Build command builder according to a given configuration.

        :param command_name: Name of the command to be built
        :type command_name: str
        :param builder_setups: Command builder configuration
        :type builder_setups: Dict[str, Any]
        :return: Command builder as specified
        :rtype: CommandBuilder
        """
        # Copy in order to avoid configuration contamination
        builder_setups = dict(builder_setups)
        command_builder = CommandBuilder(
            name=command_name, help=builder_setups.pop(HELP)
        )
        command_builder.update_from_config(builder_setups)
        return command_builder
