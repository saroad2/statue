"""Initialize configuration CLI."""
import sys
from pathlib import Path
from typing import List, Optional

import click
import git

from statue.cli.common_flags import config_path_option
from statue.cli.config.config_cli import config_cli
from statue.cli.config.interactive_adders.interactive_sources_adder import (
    InteractiveSourcesAdder,
)
from statue.cli.styled_strings import failure_style
from statue.config.configuration import Configuration
from statue.exceptions import StatueConfigurationError, UnknownTemplate
from statue.sources_finder import find_sources
from statue.templates.templates_provider import TemplatesProvider


@config_cli.command("init")
@config_path_option
@click.option(
    "-t",
    "--template",
    type=str,
    default="defaults",
    help="Configuration template name",
)
@click.option(
    "--with-sources/--no-sources",
    is_flag=True,
    default=True,
    help="Track available sources and add to configuration",
)
@click.option(
    "-e",
    "--exclude",
    type=click.Path(exists=True, path_type=Path),
    multiple=True,
    help="Sources paths that Statue will ignore tracking",
)
@click.option("-y", "interactive", flag_value=False, default=True)
@click.option(
    "--git/--no-git",
    "use_git",
    is_flag=True,
    default=True,
    help="Should use git to trace ignored files",
)
@click.option(
    "--fix-versions",
    is_flag=True,
    default=False,
    help="Fix versions in config when running",
)
@click.option(
    "-i",
    "--install",
    is_flag=True,
    default=False,
    help="Install latest version for all commands in configuration",
)
def init_config_cli(  # pylint: disable=too-many-arguments
    config: Optional[Path],
    template: str,
    with_sources: bool,
    exclude: List[Path],
    interactive: bool,
    use_git: bool,
    fix_versions: bool,
    install: bool,
):
    """
    Initialize configuration for Statue.

    By default, this command searches for sources files in the given directory (cwd by
     default) and sets them with default contexts.

    You can run this command with the "-i" flag in order to choose interactively which
     source files to track and which contexts to assign to them.
    """
    try:
        configuration = Configuration.from_file(
            TemplatesProvider.get_template_path(template)
        )
    except (UnknownTemplate, StatueConfigurationError) as error:
        click.echo(failure_style(str(error)))
        sys.exit(3)
    output_path = config if config is not None else Configuration.configuration_path()
    if with_sources:
        _update_sources(
            configuration=configuration,
            use_git=use_git,
            interactive=interactive,
            exclude=exclude,
        )
    if fix_versions or install:
        for command_builder in configuration.commands_repository:
            if install:
                command_builder.update_to_version()
            if fix_versions and command_builder.installed():
                command_builder.set_version_as_installed()
    configuration.to_toml(output_path)
    click.echo("Done!")


def _update_sources(
    configuration: Configuration, exclude: List[Path], use_git: bool, interactive: bool
):
    directory = Path.cwd()
    repo = None
    if use_git:
        try:
            repo = git.Repo(directory)
        except git.InvalidGitRepositoryError:
            pass
    sources = [
        source.relative_to(directory)
        for source in find_sources(directory, repo=repo, exclude=exclude)
    ]
    if interactive:
        InteractiveSourcesAdder.update_sources_repository(
            configuration=configuration, sources=sources, repo=repo, exclude=exclude
        )
        return
    configuration.sources_repository.track_sources(*sources)
