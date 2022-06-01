"""Add sources to configuration interactively."""
from pathlib import Path
from typing import Callable, List, Optional

import click
import click_params as clickp
import git

from statue.cli.config.interactive_adders.adders_utils import get_contexts
from statue.cli.styled_strings import (
    bullet_style,
    failure_style,
    name_style,
    source_style,
    success_style,
)
from statue.commands_filter import CommandsFilter
from statue.config.configuration import Configuration
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
        exclude: Optional[List[Path]] = None,
    ):
        """
        Add sources to configuration instance.

        :param configuration: The configuration to add sources to
        :type configuration: Configuration
        :param sources: Sources list to add to the configuration
        :type sources: List[Path]
        :param repo: Optional repository instance for avoiding ignored files.
        :type repo: Optional[Repo]
        :param exclude: Optional. Paths to be excluded from tracking
        :type exclude: Optional[List[Path]]
        """
        for source in sources:
            choices = cls._get_choices(configuration=configuration, source=source)
            if choices == NO:
                click.echo(
                    failure_style(
                        f"{source} was already defined in configuration. Skipping..."
                    )
                )
                continue
            choices_string = cls._get_choices_string(choices)
            option = click.prompt(
                f"Would you like to track {source_style(str(source))} "
                f"({choices_string}. default: {success_style('yes')})",
                type=click.Choice(choices, case_sensitive=False),
                show_choices=False,
                show_default=False,
                default="yes",
            ).lower()
            if option in EXPEND:
                cls.update_sources_repository(
                    configuration,
                    expend(source, repo=repo, exclude=exclude),
                    repo=repo,
                    exclude=exclude,
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
                contexts = get_contexts(
                    contexts_repository=configuration.contexts_repository,
                    name=str(source),
                    name_style_method=source_style,
                )
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
                f"Add {style_func(prefix)} commands to {source_style(str(source))} "
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

    @classmethod
    def _get_choices(cls, configuration: Configuration, source: Path):
        choices = []
        if source not in configuration.sources_repository.sources_list:
            choices.extend(YES)
        choices.extend(NO)
        if source.is_dir():
            choices.extend(EXPEND)
        return choices

    @classmethod
    def _get_choices_string(cls, choices):
        choices_string = f"{success_style('[Y]es')}, {failure_style('[N]o')}"
        if EXPEND[0] in choices:
            choices_string += f", {bullet_style('[E]xpend')}"
        return choices_string
