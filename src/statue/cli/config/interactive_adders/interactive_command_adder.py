"""Add commands to configuration interactively."""
from typing import Dict, List, Optional, Set

import click
import click_params as clickp

from statue.cli.config.interactive_adders.adders_utils import (
    get_context,
    get_contexts,
    get_help_string,
)
from statue.cli.styled_strings import bullet_style, failure_style, name_style
from statue.command_builder import CommandBuilder, ContextSpecification
from statue.config.commands_repository import CommandsRepository
from statue.config.configuration import Configuration
from statue.config.contexts_repository import ContextsRepository
from statue.context import Context
from statue.exceptions import InconsistentConfiguration


class InteractiveCommandAdder:
    """Singleton class for adding and editing commands in configuration instance."""

    @classmethod
    def add_command(cls, configuration: Configuration):
        """
        Add commands interactively to commands repository.

        :param configuration: Statue configuration
        :type configuration: Configuration
        """
        name = cls.get_command_name(configuration.commands_repository)
        help_string = get_help_string(name)
        default_args = cls.get_args(name, args_type="default")
        version = cls.get_version(name)
        preoccupied_contexts = set()
        required_contexts = get_contexts(
            name=name,
            contexts_repository=configuration.contexts_repository,
            name_style_method=name_style,
            contexts_type="required",
        )
        preoccupied_contexts.update(required_contexts)
        allowed_contexts = get_contexts(
            name=name,
            contexts_repository=configuration.contexts_repository,
            name_style_method=name_style,
            contexts_type="allowed",
            preoccupied_contexts=preoccupied_contexts,
        )
        preoccupied_contexts.update(allowed_contexts)
        denied_contexts = get_contexts(
            name=name,
            contexts_repository=configuration.contexts_repository,
            name_style_method=name_style,
            contexts_type="denied",
            preoccupied_contexts=preoccupied_contexts,
        )
        preoccupied_contexts.update(denied_contexts)
        contexts_specifications = cls.get_contexts_specifications(
            name=name,
            contexts_repository=configuration.contexts_repository,
            preoccupied_contexts=preoccupied_contexts,
        )
        configuration.commands_repository.add_command_builders(
            CommandBuilder(
                name=name,
                help=help_string,
                default_args=default_args,
                version=version,
                required_contexts=required_contexts,
                allowed_contexts=allowed_contexts,
                denied_contexts=denied_contexts,
                contexts_specifications=contexts_specifications,
            )
        )

    @classmethod
    def edit_command(cls, name: str, configuration: Configuration):
        """
        Edit a command interactively in commands repository.

        :param name: Name of the command to edit
        :type name: str
        :param configuration: Statue configuration
        :type configuration: Configuration
        """
        command_builder = configuration.commands_repository[name]
        command_builder.help = get_help_string(name)
        command_builder.default_args = cls.get_args(name, args_type="default")
        command_builder.version = cls.get_version(name)
        command_builder.reset_all_contexts()
        preoccupied_contexts = set()
        command_builder.required_contexts = get_contexts(  # type: ignore
            name=name,
            contexts_repository=configuration.contexts_repository,
            name_style_method=name_style,
            contexts_type="required",
        )
        preoccupied_contexts.update(command_builder.required_contexts)
        command_builder.allowed_contexts = get_contexts(  # type: ignore
            name=name,
            contexts_repository=configuration.contexts_repository,
            name_style_method=name_style,
            contexts_type="allowed",
            preoccupied_contexts=preoccupied_contexts,
        )
        preoccupied_contexts.update(command_builder.allowed_contexts)
        command_builder.denied_contexts = get_contexts(  # type: ignore
            name=name,
            contexts_repository=configuration.contexts_repository,
            name_style_method=name_style,
            contexts_type="denied",
            preoccupied_contexts=preoccupied_contexts,
        )
        preoccupied_contexts.update(command_builder.denied_contexts)
        command_builder.contexts_specifications = cls.get_contexts_specifications(
            name=name,
            contexts_repository=configuration.contexts_repository,
            preoccupied_contexts=preoccupied_contexts,
        )

    @classmethod
    def get_command_name(cls, commands_repository: CommandsRepository) -> str:
        """
        Get context name interactively from user.

        :param commands_repository: Commands repository to check
            pre-existing commands in
        :type commands_repository: CommandsRepository
        :return: new command name
        :rtype: str
        """
        name = ""
        while name == "":
            name = click.prompt(
                f"Please choose {bullet_style('command')} name",
                default="",
                show_default=False,
            )
            name = name.strip()
            if name in commands_repository:
                click.echo(failure_style(f"{name} already exists in repository!"))
                name = ""
        return name

    @classmethod
    def get_args(cls, name: str, args_type: Optional[str] = None) -> List[str]:
        """
        Get default arguments for command from user.

        :param name: Name of the command
        :type name: str
        :param args_type: Type of the arguments to get. Optional
        :type args_type: Optional[str]
        :return: List of default arguments
        :rtype: List[str]
        """
        arguments_title = "arguments" if args_type is None else f"{args_type} arguments"
        default_args = click.prompt(
            f"Please add {arguments_title} of {name_style(name)} separated by spaces "
            "(press enter to skip)",
            default="",
            type=clickp.StringListParamType(separator=" "),
            show_default=False,
        )
        default_args = [arg for arg in default_args if arg.strip() != ""]
        return default_args

    @classmethod
    def get_version(cls, name: str) -> Optional[str]:
        """
        Get version string for command from user.

        Press enter to return empty version

        :param name: Name of the command
        :type name: str
        :return: Optional version
        :rtype: Optional[str]
        """
        version = click.prompt(
            f"Please add {name_style(name)} version (press enter to skip)",
            default="",
            type=str,
            show_default=False,
        )
        version = version.strip()
        return None if version == "" else version

    @classmethod
    def get_contexts_specifications(
        cls,
        name: str,
        contexts_repository: ContextsRepository,
        preoccupied_contexts: Set[Context],
    ) -> Dict[Context, ContextSpecification]:
        """
        Get contexts specifications dictionary from user.

        :param name: Name of the command to get contexts specifications for
        :type name: str
        :param contexts_repository: Contexts repository to get contexts from
        :type contexts_repository: ContextsRepository
        :param preoccupied_contexts: Set of already taken contexts
            that can't be specified
        :type preoccupied_contexts: Set[Context]
        :return: Dictionary from contexts to their specifications
        :rtype: Dict[Context, ContextSpecification]
        """
        contexts_specification = {}
        while True:
            context = get_context(
                contexts_repository=contexts_repository,
                name=name,
                name_style_method=name_style,
                context_type="specified",
                preoccupied_contexts=preoccupied_contexts,
            )
            if context is None:
                break
            contexts_specification[context] = cls.get_context_specification(
                context.name
            )
            preoccupied_contexts.add(context)
        return contexts_specification

    @classmethod
    def get_context_specification(cls, name: str) -> ContextSpecification:
        """
        Get context specification for a given context name.

        :param name: Name of the context to be specified
        :type name: str
        :return: Context specification for the given context
        :rtype: ContextSpecification
        """
        while True:
            args = cls.get_args(name, args_type="override")
            added_args = cls.get_args(name, args_type="added")
            clear_args = click.confirm(
                f"Would you like {name_style(name)} to clear arguments?", default=False
            )
            try:
                return ContextSpecification(
                    args=(args if len(args) != 0 else None),
                    add_args=(added_args if len(added_args) != 0 else None),
                    clear_args=clear_args,
                )
            except InconsistentConfiguration as error:
                click.echo(failure_style(str(error)))
