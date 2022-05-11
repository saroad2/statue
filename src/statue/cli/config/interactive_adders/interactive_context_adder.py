"""Add contexts to configuration interactively."""
from typing import List, Optional

import click
import click_params as clickp

from statue.cli.config.interactive_adders.adders_utils import get_help_string
from statue.cli.styled_strings import failure_style, name_style
from statue.config.contexts_repository import ContextsRepository
from statue.context import Context


class InteractiveContextAdder:
    """Singleton class for adding contexts to configuration instance."""

    @classmethod
    def add_context(cls, contexts_repository: ContextsRepository):
        """
        Add context interactively to context repository.

        :param contexts_repository: contexts repository to add context to
        :type contexts_repository: ContextsRepository
        """
        name = cls.get_context_name(contexts_repository)
        help_string = get_help_string(name)
        aliases = cls.get_aliases(name=name, contexts_repository=contexts_repository)
        parent = cls.get_parent(
            name=name, aliases=aliases, contexts_repository=contexts_repository
        )
        allowed_by_default = click.confirm(
            f"Would you like {name_style(name)} context to be allowed by default?",
            default=False,
            show_default=True,
        )
        context = Context(
            name=name,
            help=help_string,
            aliases=aliases,
            parent=parent,
            allowed_by_default=allowed_by_default,
        )
        contexts_repository.add_contexts(context)

    @classmethod
    def edit_context(cls, name: str, contexts_repository: ContextsRepository):
        """
        Edit existing context in context repository.

        :param name: Name of the context to edit
        :type name: str
        :param contexts_repository: Contexts repository instance to edit context in
        :type contexts_repository: ContextsRepository
        """
        context = contexts_repository[name]
        context.clear_aliases()
        context.help = get_help_string(name)
        context.aliases = cls.get_aliases(
            name=name, contexts_repository=contexts_repository
        )
        context.parent = cls.get_parent(
            name=name, aliases=context.aliases, contexts_repository=contexts_repository
        )
        context.allowed_by_default = click.confirm(
            f"Would you like {name_style(name)} context to be allowed by default?",
            default=False,
            show_default=True,
        )

    @classmethod
    def get_context_name(cls, contexts_repository: ContextsRepository) -> str:
        """
        Get context name interactively from user.

        :param contexts_repository: Context repository to check pre-existing contexts in
        :type contexts_repository: ContextsRepository
        :return: new context name
        :rtype: str
        """
        name = ""
        while name == "":
            name = click.prompt(
                "Please choose context name",
                default="",
                show_default=False,
            )
            name = name.strip()
            if name in contexts_repository:
                click.echo(failure_style(f"{name} already exists in repository!"))
                name = ""
        return name

    @classmethod
    def get_aliases(
        cls, name: str, contexts_repository: ContextsRepository
    ) -> List[str]:
        """
        Get aliases for context.

        :param name: name of the context to get aliases for
        :type name: str
        :param contexts_repository: Context repository to check pre-existing contexts in
        :type contexts_repository: ContextsRepository
        :return: new context aliases
        :rtype: List[str]
        """
        aliases = None
        while aliases is None:
            aliases = click.prompt(
                f"Please add aliases of {name_style(name)} separated by commas "
                "(press enter to skip)",
                default="",
                type=clickp.StringListParamType(),
                show_default=False,
            )
            aliases = [alias.strip() for alias in aliases if alias.strip() != ""]
            if name in aliases:
                aliases.remove(name)
            predefined_aliases = [
                alias for alias in aliases if alias in contexts_repository
            ]
            if len(predefined_aliases) != 0:
                click.echo(
                    failure_style(
                        "Could not set the following aliases since they are "
                        f"already taken: {','.join(predefined_aliases)}"
                    )
                )
                aliases = None
        return aliases

    @classmethod
    def get_parent(
        cls,
        name: str,
        aliases: List[str],
        contexts_repository: ContextsRepository,
    ) -> Optional[Context]:
        """
        Get parent for the new context.

        :param name: Context name to get parent for
        :type name: str
        :param aliases: Aliases list for the context
        :type aliases: List[str]
        :param contexts_repository: Contexts repository to check existing contexts
        :type contexts_repository: ContextsRepository
        :return: Optional context parent
        :rtype: Optional[Context]
        """
        parent_name = None
        while parent_name is None:
            parent_name = click.prompt(
                "Please choose parent context (press enter to skip)",
                type=str,
                default="",
                show_default=False,
            )
            parent_name = parent_name.strip()
            if parent_name == "":
                return None
            if parent_name == name or parent_name in aliases:
                click.echo(failure_style(f"{name} can't be parent of itself"))
                parent_name = None
                continue
            if parent_name not in contexts_repository:
                click.echo(failure_style(f"{parent_name} doesn't exist."))
                parent_name = None
                continue
        return contexts_repository[parent_name]
