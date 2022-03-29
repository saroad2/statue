"""Add sources to configuration interactively."""
from pathlib import Path
from typing import Callable, List, Optional

import click
import click_params as clickp
import git

from statue.cli.styled_strings import (
    bullet_style,
    failure_style,
    name_style,
    source_style,
    success_style,
)
from statue.commands_filter import CommandsFilter
from statue.config.configuration import Configuration
from statue.context import Context
from statue.exceptions import UnknownContext
from statue.sources_finder import expend

YES = ["y", "yes"]
NO = ["n", "no"]
EXPEND = ["e", "expend"]


class InteractiveSourcesAdder:
    """Singleton class for adding sources to configuration instance."""

    @classmethod
    def update_sources_repository(
        cls,
        configuration: Configuration,
        sources: List[Path],
        repo: Optional[git.Repo] = None,
    ):
        """
        Add sources to configuration instance.

        :param configuration: The configuration to add sources to
        :type configuration: Configuration
        :param sources: Sources list to add to the configuration
        :type sources: List[Path]
        :param repo: Optional repository instance for avoiding ignored files.
        :type repo: Optional[Repo]
        """
        for source in sources:
            choices = YES + NO
            choices_string = f"{success_style('[Y]es')}, {failure_style('[N]o')}"
            if source.is_dir():
                choices.extend(EXPEND)
                choices_string += f", {bullet_style('[E]xpend')}"
            option = click.prompt(
                f"Would you like to track {source_style(source)} ({choices_string}. "
                f"default: {success_style('yes')})",
                type=click.Choice(choices, case_sensitive=False),
                show_choices=False,
                show_default=False,
                default="yes",
            ).lower()
            if option in EXPEND:
                cls.update_sources_repository(
                    configuration,
                    expend(source, repo=repo),
                    repo=repo,
                )
            if option not in YES:
                continue
            configuration.sources_repository[source] = cls.get_filter(
                configuration, source
            )

    @classmethod
    def get_filter(cls, configuration: Configuration, source: Path) -> CommandsFilter:
        """
        Get a commands filter from the user for the specified source.

        :param configuration: Configuration instance
        :type configuration: Configuration
        :param source: Source to get filter for
        :type source: Path
        :return: Commands filter for the source
        :rtype: CommandsFilter
        """
        while True:
            try:
                contexts = cls.get_contexts(configuration, source)
                allowed_commands = cls.get_commands(
                    configuration, source, prefix="allowed", style_func=success_style
                )
                denied_commands = cls.get_commands(
                    configuration, source, prefix="denied", style_func=failure_style
                )
                return CommandsFilter(
                    contexts=contexts,
                    allowed_commands=allowed_commands,
                    denied_commands=denied_commands,
                )
            except ValueError as error:
                click.echo(failure_style(str(error)))
                click.echo("Try again...")

    @classmethod
    def get_contexts(cls, configuration: Configuration, source: Path) -> List[Context]:
        """
        Get contexts from user for specific source.

        :param configuration: Configuration instance
        :type configuration: Configuration
        :param source: Source to get contexts for
        :type source: Path
        :return: Sources list for source
        :rtype: List[Context]
        """
        if len(configuration.contexts_repository) == 0:
            return []
        contexts_options = ", ".join(
            [name_style(context.name) for context in configuration.contexts_repository]
        )
        while True:
            try:
                context_names = click.prompt(
                    f"Add {bullet_style('contexts')} to {source_style(source)} "
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
                return [
                    configuration.contexts_repository[context]
                    for context in context_names
                ]
            except UnknownContext as error:
                click.echo(failure_style(str(error)))

    @classmethod
    def get_commands(
        cls,
        configuration: Configuration,
        source: Path,
        prefix: str,
        style_func: Callable[[str], str],
    ) -> Optional[List[str]]:
        """
        Get commands list from user for specific source.

        :param configuration: Configuration instance
        :type configuration: Configuration
        :param source: Source to get commands for
        :type source: Path
        :param prefix: Commands type to look for (allowed/denied)
        :type prefix: str
        :param style_func: Styling function for prefix
        :type style_func: Callable[[str], str]
        :return: Sources list for source
        :rtype: List[Context]
        """
        if len(configuration.commands_repository) == 0:
            return None
        commands_options = ", ".join(
            [
                name_style(command_builder.name)
                for command_builder in configuration.commands_repository
            ]
        )
        while True:
            command_names = click.prompt(
                f"Add {style_func(prefix)} commands to {source_style(source)} "
                f"(options: [{commands_options}], "
                f"No specified {prefix} commands by default)",
                default="",
                type=clickp.StringListParamType(),
                show_default=False,
            )
            command_names = [
                command_name.strip()
                for command_name in command_names
                if command_name.strip() != ""
            ]
            if len(command_names) == 0:
                return None
            unknown_commands = [
                command_name
                for command_name in command_names
                if command_name not in configuration.commands_repository
            ]
            if len(unknown_commands) != 0:
                click.echo(
                    failure_style(
                        "Could not find the following commands: "
                        f"{', '.join(unknown_commands)}"
                    )
                )
                continue
            return command_names
