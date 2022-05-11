"""Utility module for interactive adders."""
from typing import Callable, List, Optional, Set

import click
import click_params as clickp

from statue.cli.styled_strings import bullet_style, failure_style, name_style
from statue.config.contexts_repository import ContextsRepository
from statue.context import Context
from statue.exceptions import UnknownContext


def get_help_string(name: str) -> str:
    """
    Get help string for an object.

    :param name: Name of the object to get help for
    :type name: str
    :return: help string for the object
    :rtype: str
    """
    help_string = ""
    while help_string == "":
        help_string = click.prompt(
            f"Please add help string for {name_style(name)}",
            default="",
            show_default=False,
        )
        help_string = help_string.strip()
        if help_string == "":
            click.echo(failure_style("Help string cannot be empty!"))
    return help_string


def get_context(
    contexts_repository: ContextsRepository,
    name: str,
    preoccupied_contexts: Set[Context],
    name_style_method: Callable[[str], str],
    context_type: Optional[str] = None,
) -> Optional[Context]:
    """
    Get a context from user for specific configuration (command or source).

    :param contexts_repository: Contexts repository to get contexts from
    :type contexts_repository: ContextsRepository
    :param name: Configuration object to get contexts for
    :type name: str
    :param name_style_method: Styling method for name.
    :type name_style_method: Callable[[str], str]
    :param context_type: Optional type of the desired contexts.
    :type context_type: Optional[str]
    :param preoccupied_contexts: Contexts that cannot be set by the users.
    :type preoccupied_contexts: Set[Context]
    :return: Contexts list for given item
    :rtype: List[Context]
    """
    if len(contexts_repository) == 0:
        return None
    contexts_options = ", ".join(
        [
            name_style(context.name)
            for context in contexts_repository
            if context not in preoccupied_contexts
        ]
    )
    name = name_style_method(name)
    context_title = "context" if context_type is None else f"{context_type} context"
    while True:
        try:
            context_name = click.prompt(
                f"Add {bullet_style(context_title)} to {name} "
                f"(options: [{contexts_options}], press enter to skip)",
                default="",
                type=str,
                show_default=False,
            ).strip()
            if context_name == "":
                return None
            context = contexts_repository[context_name]
            if context in preoccupied_contexts:
                click.echo(
                    failure_style(
                        f"Could not set {context_name} as specifies context "
                        "because it is preoccupied."
                    )
                )
                continue
            return context
        except UnknownContext as error:
            click.echo(failure_style(str(error)))


def get_contexts(
    contexts_repository: ContextsRepository,
    name: str,
    name_style_method: Callable[[str], str],
    contexts_type: Optional[str] = None,
    preoccupied_contexts: Optional[Set[Context]] = None,
) -> List[Context]:
    """
    Get contexts from user for specific configuration (command or source).

    :param contexts_repository: Contexts repository to get contexts from
    :type contexts_repository: ContextsRepository
    :param name: Configuration object to get contexts for
    :type name: str
    :param name_style_method: Styling method for name.
    :type name_style_method: Callable[[str], str]
    :param contexts_type: Optional type of the desired contexts.
    :type contexts_type: Optional[str]
    :param preoccupied_contexts: Contexts that cannot be set by the users. Optional.
    :type preoccupied_contexts: Optional[Set[Context]]:
    :return: Contexts list for given item
    :rtype: List[Context]
    """
    if len(contexts_repository) == 0:
        return []
    preoccupied_contexts = (
        set() if preoccupied_contexts is None else preoccupied_contexts
    )
    contexts_options = ", ".join(
        [
            name_style(context.name)
            for context in contexts_repository
            if context not in preoccupied_contexts
        ]
    )
    name = name_style_method(name)
    contexts_title = (
        "contexts" if contexts_type is None else f"{contexts_type} contexts"
    )
    while True:
        try:
            context_names = click.prompt(
                f"Add {bullet_style(contexts_title)} to {name} "
                f"(options: [{contexts_options}])",
                default="",
                type=clickp.StringListParamType(),
                show_default=False,
            )
            context_names = [
                context_name.strip()
                for context_name in context_names
                if context_name.strip() != ""
            ]
            contexts = [contexts_repository[context] for context in context_names]
            unavailable_contexts = [
                context.name for context in contexts if context in preoccupied_contexts
            ]
            if len(unavailable_contexts) > 0:
                unavailable_contexts_string = ", ".join(
                    context_name for context_name in unavailable_contexts
                )
                click.echo(
                    failure_style(
                        "The following contexts could not be set: "
                        f"{unavailable_contexts_string}"
                    )
                )
                continue
            return contexts
        except UnknownContext as error:
            click.echo(failure_style(str(error)))
